from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import inline
from app.bot.states import CreatePromoSG, EditPromoSG, DeletePromoSG, InfoPromoSG
# from app.services import PromoService, UserPromoService, UserService
from app.bot.filters import AdminFilter

router = Router()
router.message.filter(AdminFilter())


#CREATE PROMO HANDLERS
@router.message(CreatePromoSG.NAME)
async def promo_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer('Введите сумму, которую получит пользователь на баланс после ввода промокода')
    await state.set_state(CreatePromoSG.GIFT_AMOUNT)


@router.message(CreatePromoSG.GIFT_AMOUNT)
async def promo_gift_amount_handler(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(gift_amount=message.text)
        await message.answer('Введите количество использований')
        await state.set_state(CreatePromoSG.USES)
    else:
        await message.answer('Введите число!')


@router.message(CreatePromoSG.USES)
async def promo_gift_amount_handler(
    message: Message,
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    if message.text.isdigit():
        data = await state.get_data()
        # await promo_service.add_promo(name=data['name'], gift_amount=data['gift_amount'], uses=int(message.text))
        await message.answer('Вы успешно добавили промокод!')
        await state.clear()
    else:
        await message.answer('Введите число!')


@router.message(EditPromoSG.NAME)
async def edit_promo_name_handler(
    message: Message,
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    await state.clear()
    name = message.text
    if name.isdigit():
        pass
        # promo = await promo_service.get_promo_by_id(id=name)
        # await message.answer(f'Номер: №{promo.id}\nНазвание: {promo.name}\nСумма: {promo.gift_amount}₽\nКол-во использований: {promo.uses}\n\nВыберите один из вариантов:', reply_markup=inline.edit_promo_kb_markup(name=message.text))
    else:
        pass
        # promo = await promo_service.get_promo_by_name(name=name)
        # await message.answer(f'Номер: №{promo.id}\nНазвание: {promo.name}\nСумма: {promo.gift_amount}₽\nКол-во использований: {promo.uses}\n\nВыберите один из вариантов:', reply_markup=inline.edit_promo_kb_markup(name=message.text))




@router.message(EditPromoSG.NEW_GIFT_AMOUNT)
async def new_amount_handler(
    message: Message,
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    data = await state.get_data()
    if data['name'].isdigit():
        pass
        # await promo_service.update_promo_by_id(id=data['name'], gift_amount=int(message.text))
    else:
        pass
        # await promo_service.update_promo_by_name(name=data['name'], gift_amount=int(message.text))
    await message.answer('Новое значение было успешно установлено')
    await state.clear()


@router.message(EditPromoSG.NEW_USES)
async def new_uses_handler(
    message: Message, 
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    data = await state.get_data()
    if data['name'].isdigit():
        # await promo_service.update_promo_by_id(id=data['name'], uses=int(message.text))
        pass
    else:
        # await promo_service.update_promo_by_name(name=data['name'], uses=int(message.text))
        pass
    await message.answer('Новое значение было успешно установлено')
    await state.clear()


@router.message(InfoPromoSG.NAME)
async def show_info_promo_handler(
    message: Message,
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    await state.clear()
    name = message.text
    if name.isdigit():
        # promo = await promo_service.get_promo_by_id(id=name)
        # await message.answer(f'Номер: №{promo.id}\nНазвание: {promo.name}\nСумма: {promo.gift_amount}₽\nКол-во оставшихся использований: {promo.uses}')
        pass
    else:
        pass
        # promo = await promo_service.get_promo_by_name(name=name)
        # await message.answer(f'Номер: №{promo.id}\nНазвание: {promo.name}\nСумма: {promo.gift_amount}₽\nКол-во оставшихся использований: {promo.uses}')



@router.message(DeletePromoSG.NAME)
async def delete_promo_handler(
    message: Message,
    state: FSMContext,
    # promo_service: FromDishka[PromoService]
) -> None:
    await state.clear()
    name = message.text
    try:
        if name.isdigit():
            # await promo_service.update_promo_by_id(id=int(name), status='неактивный')
            await message.answer('Вы успешно удалили промокод')
        else:
            # await promo_service.update_promo_by_name(name=name, status='неактивный')
            await message.answer('Вы успешно удалили промокод')
    except Exception as _ex:
        print(_ex)
        await message.answer('Упс... Что-то пошло не так при удалении кода')
