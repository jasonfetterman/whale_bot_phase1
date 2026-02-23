from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import json
import os

from services.wallets import (
    add_wallet,
    remove_wallet,
    get_wallets,
    update_wallet_label,
    set_wallet_enabled,
    set_wallet_chains,
)
from bot.keyboards.main_menu import get_main_menu
from services.plan_checker import can_track_wallets
from services.user_tiers import get_tier

router = Router()

ALL_CHAINS = ["eth", "bsc", "polygon", "arbitrum", "base"]
PRESET_FILE = "data/wallet_presets.json"


# ---------- PRESET STORAGE ----------

def _load_presets():
    if not os.path.exists(PRESET_FILE):
        return {}
    with open(PRESET_FILE, "r") as f:
        return json.load(f)


def _save_presets(data):
    with open(PRESET_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- FSM ----------

class WalletFSM(StatesGroup):
    waiting_for_address = State()
    waiting_for_label = State()
    waiting_for_chain_address = State()
    waiting_for_chain_value = State()
    waiting_for_preset_name = State()
    waiting_for_preset_load = State()


# ---------- MENUS ----------

wallet_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add Wallet")],
        [KeyboardButton(text="⛓ Set Chains")],
        [KeyboardButton(text="💾 Save Preset")],
        [KeyboardButton(text="📂 Load Preset")],
        [KeyboardButton(text="📄 My Wallets")],
        [KeyboardButton(text="⬅ Back to Menu")],
    ],
    resize_keyboard=True,
)

preset_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅ Back to Wallets")],
    ],
    resize_keyboard=True,
)


# ---------- ENTRY ----------

@router.message(StateFilter("*"), F.text == "👛 Wallets")
async def wallets_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Wallet management:", reply_markup=wallet_menu)


@router.message(StateFilter("*"), F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Main menu:", reply_markup=get_main_menu())


@router.message(StateFilter("*"), F.text == "⬅ Back to Wallets")
async def back_to_wallets(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Wallet management:", reply_markup=wallet_menu)


# ---------- ADD WALLET ----------

@router.message(StateFilter("*"), F.text == "➕ Add Wallet")
async def add_wallet_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_address)
    await message.answer("Send wallet address:")


@router.message(WalletFSM.waiting_for_address)
async def add_wallet_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip().lower())
    await state.set_state(WalletFSM.waiting_for_label)
    await message.answer("Optional label? Send label or `-` to skip.")


@router.message(WalletFSM.waiting_for_label)
async def add_wallet_label(message: Message, state: FSMContext):
    data = await state.get_data()
    address = data["address"]
    label = None if message.text.strip() == "-" else message.text.strip()

    wallets = await get_wallets(message.chat.id)
    if any(w["address"] == address for w in wallets):
        await state.clear()
        await message.answer("⚠️ Wallet already exists.", reply_markup=wallet_menu)
        return

    allowed = await can_track_wallets(message.from_user.id, len(wallets))
    if not allowed:
        await state.clear()
        await message.answer("🚫 Wallet limit reached.", reply_markup=wallet_menu)
        return

    await add_wallet(message.chat.id, address, label)
    await state.clear()
    await message.answer("Wallet added.", reply_markup=wallet_menu)


# ---------- PRESETS ----------

@router.message(F.text == "💾 Save Preset")
async def save_preset_start(message: Message, state: FSMContext):
    tier = await get_tier(message.from_user.id)
    if tier not in ("elite", "super_elite"):
        return

    await state.clear()
    await state.set_state(WalletFSM.waiting_for_preset_name)
    await message.answer("Preset name?", reply_markup=preset_menu)


@router.message(WalletFSM.waiting_for_preset_name)
async def save_preset_name(message: Message, state: FSMContext):
    name = message.text.strip()
    wallets = await get_wallets(message.chat.id)

    data = _load_presets()
    user_id = str(message.from_user.id)
    data.setdefault(user_id, {})[name] = wallets
    _save_presets(data)

    await state.clear()
    await message.answer(f"Preset `{name}` saved.", reply_markup=wallet_menu, parse_mode="Markdown")


@router.message(F.text == "📂 Load Preset")
async def load_preset_start(message: Message, state: FSMContext):
    tier = await get_tier(message.from_user.id)
    if tier not in ("elite", "super_elite"):
        return

    data = _load_presets().get(str(message.from_user.id), {})
    if not data:
        await message.answer("No presets saved.", reply_markup=wallet_menu)
        return

    await state.set_state(WalletFSM.waiting_for_preset_load)
    await message.answer(
        "Send preset name:\n" + "\n".join(f"• {k}" for k in data.keys()),
        reply_markup=preset_menu,
    )


@router.message(WalletFSM.waiting_for_preset_load)
async def load_preset(message: Message, state: FSMContext):
    name = message.text.strip()
    data = _load_presets().get(str(message.from_user.id), {})

    if name not in data:
        await state.clear()
        await message.answer("Preset not found.", reply_markup=wallet_menu)
        return

    for w in data[name]:
        try:
            await add_wallet(
                message.chat.id,
                w["address"],
                w.get("label"),
            )
            await set_wallet_chains(
                message.chat.id,
                w["address"],
                w.get("chains", ALL_CHAINS),
            )
        except Exception:
            pass

    await state.clear()
    await message.answer(f"Preset `{name}` loaded.", reply_markup=wallet_menu, parse_mode="Markdown")
