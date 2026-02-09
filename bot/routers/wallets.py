from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from services.wallets import (
    add_wallet,
    remove_wallet,
    get_wallets,
    update_wallet_label,
    set_wallet_enabled,
    set_wallet_chains,
)
from bot.keyboards.main_menu import get_main_menu
from services.plan_checker import can_track_wallets  # ✅ PLAN CHECK

router = Router()

ALL_CHAINS = ["eth", "bsc", "polygon", "arbitrum", "base"]


class WalletFSM(StatesGroup):
    waiting_for_address = State()
    waiting_for_label = State()
    waiting_for_remove = State()
    waiting_for_label_edit_address = State()
    waiting_for_label_edit_value = State()
    waiting_for_toggle_address = State()
    waiting_for_chain_address = State()
    waiting_for_chain_value = State()


wallet_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add Wallet")],
        [KeyboardButton(text="✏ Edit Label")],
        [KeyboardButton(text="🔔 Toggle Alerts")],
        [KeyboardButton(text="⛓ Set Chains")],
        [KeyboardButton(text="➖ Remove Wallet")],
        [KeyboardButton(text="📄 My Wallets")],
        [KeyboardButton(text="⬅ Back to Menu")],
    ],
    resize_keyboard=True,
)

# -------- ENTRY / EXIT --------

@router.message(StateFilter("*"), F.text == "👛 Wallets")
async def wallets_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Wallet management:", reply_markup=wallet_menu)


@router.message(StateFilter("*"), F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Main menu:", reply_markup=get_main_menu())

# -------- ADD WALLET --------

@router.message(StateFilter("*"), F.text == "➕ Add Wallet")
async def add_wallet_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_address)
    await message.answer("Send wallet address:")


@router.message(WalletFSM.waiting_for_address)
async def add_wallet_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(WalletFSM.waiting_for_label)
    await message.answer("Optional label? Send label or `-` to skip.")


@router.message(WalletFSM.waiting_for_label)
async def add_wallet_label(message: Message, state: FSMContext):
    data = await state.get_data()
    label = None if message.text.strip() == "-" else message.text.strip()

    telegram_id = message.from_user.id
    wallets = await get_wallets(message.chat.id)
    current_wallet_count = len(wallets)

    allowed = await can_track_wallets(telegram_id, current_wallet_count)
    if not allowed:
        await state.clear()
        await message.answer(
            "🚫 Wallet limit reached.\n\nUpgrade to unlock more wallets.",
            reply_markup=wallet_menu,
        )
        return

    await add_wallet(message.chat.id, data["address"], label)
    await state.clear()
    await message.answer("Wallet added.", reply_markup=wallet_menu)

# -------- EDIT LABEL --------

@router.message(StateFilter("*"), F.text == "✏ Edit Label")
async def edit_label_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_label_edit_address)
    await message.answer("Send wallet address to relabel:")


@router.message(WalletFSM.waiting_for_label_edit_address)
async def edit_label_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(WalletFSM.waiting_for_label_edit_value)
    await message.answer("Send new label (or `-` to clear):")


@router.message(WalletFSM.waiting_for_label_edit_value)
async def edit_label_value(message: Message, state: FSMContext):
    data = await state.get_data()
    label = None if message.text.strip() == "-" else message.text.strip()
    await update_wallet_label(message.chat.id, data["address"], label)
    await state.clear()
    await message.answer("Label updated.", reply_markup=wallet_menu)

# -------- TOGGLE ALERTS --------

@router.message(StateFilter("*"), F.text == "🔔 Toggle Alerts")
async def toggle_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_toggle_address)
    await message.answer("Send wallet address to enable / disable alerts:")


@router.message(WalletFSM.waiting_for_toggle_address)
async def toggle_wallet(message: Message, state: FSMContext):
    address = message.text.strip().lower()
    wallets = await get_wallets(message.chat.id)
    target = next((w for w in wallets if w["address"] == address), None)

    if target:
        new_state = not target["enabled"]
        await set_wallet_enabled(message.chat.id, address, new_state)
        await message.answer(
            f"Alerts {'enabled ✅' if new_state else 'disabled ❌'}.",
            reply_markup=wallet_menu,
        )
    else:
        await message.answer("Wallet not found.", reply_markup=wallet_menu)

    await state.clear()

# -------- SET CHAINS --------

@router.message(StateFilter("*"), F.text == "⛓ Set Chains")
async def set_chains_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_chain_address)
    await message.answer(
        "Send wallet address to set chains.\nAvailable: eth, bsc, polygon, arbitrum, base"
    )


@router.message(WalletFSM.waiting_for_chain_address)
async def set_chains_address(message: Message, state: FSMContext):
    address = message.text.strip().lower()
    wallets = await get_wallets(message.chat.id)
    target = next((w for w in wallets if w["address"] == address), None)

    if not target:
        await message.answer("Wallet not found.", reply_markup=wallet_menu)
        await state.clear()
        return

    await state.update_data(address=address)
    await state.set_state(WalletFSM.waiting_for_chain_value)
    await message.answer(
        f"Current chains: {','.join(target['chains'])}\nSend new comma-separated chains:"
    )


@router.message(WalletFSM.waiting_for_chain_value)
async def set_chains_value(message: Message, state: FSMContext):
    data = await state.get_data()
    chains = [c.strip() for c in message.text.split(",") if c.strip() in ALL_CHAINS]
    await set_wallet_chains(message.chat.id, data["address"], chains)
    await state.clear()
    await message.answer("Chains updated.", reply_markup=wallet_menu)

# -------- REMOVE / LIST --------

@router.message(StateFilter("*"), F.text == "➖ Remove Wallet")
async def remove_wallet_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WalletFSM.waiting_for_remove)
    await message.answer("Send wallet address to remove:")


@router.message(WalletFSM.waiting_for_remove)
async def remove_wallet_confirm(message: Message, state: FSMContext):
    await remove_wallet(message.chat.id, message.text.strip())
    await state.clear()
    await message.answer("Wallet removed.", reply_markup=wallet_menu)


@router.message(StateFilter("*"), F.text == "📄 My Wallets")
async def list_wallets(message: Message):
    wallets = await get_wallets(message.chat.id)
    if not wallets:
        await message.answer("No wallets tracked.", reply_markup=wallet_menu)
        return

    lines = []
    for w in wallets:
        lines.append(
            f"{w['address']} — "
            f"{w['label'] or 'no label'} — "
            f"{'ON' if w['enabled'] else 'OFF'} — "
            f"{','.join(w['chains'])}"
        )

    await message.answer("\n".join(lines), reply_markup=wallet_menu)
