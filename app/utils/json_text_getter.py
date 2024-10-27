import json
import os
import uuid
from typing import Optional
from app.schema import Product

from uuid import UUID

from pydantic import BaseModel


class CreateOrderDTO(BaseModel):
    product_id: UUID
    additional_data: dict


def get_json_text(key: str) -> Optional[str]:
    with open(os.path.normpath('src/files/texts.json'), encoding="utf-8") as f:
        data = json.load(f)

        return data.get(key)
    

def get_order_info_text(
    user_id: int,
    order_id: uuid.UUID,
    order_data: CreateOrderDTO,
    product: Product,
) -> Optional[str]:
    if product.game_name in ('Clash of Clans', 'Clash Royale', 'Brawl Stars', 'Squad Busters'):
        return get_json_text('supercell_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            category=product.category,
            product_name=product.name,
            product_price=product.price,
            email=order_data.additional_data.get('email'),
            code=order_data.additional_data.get('code'),
        )
    elif product.game_name == 'Roblox':
        return get_json_text('roblox_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            category=product.category,
            product_name=product.name,
            product_price=product.price,
            email=order_data.additional_data.get('login'),
            password=order_data.additional_data.get('password'),
            two_factor_code=order_data.additional_data.get('two_factor_code') if order_data.additional_data.get('two_factor_code') else '-',
        )
    elif product.game_name == 'PUBG':
        return get_json_text('pubg_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            category=product.category,
            product_name=product.name,
            product_price=product.price,
            pubg_id=order_data.additional_data.get('pubg_id'),
        )
    elif product.game_name == 'Stumble Guys':
        return get_json_text('stumble_guys_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            category=product.category,
            product_name=product.name,
            product_price=product.price,
            nickname=order_data.additional_data.get('nickname'),
        )
    else:
        return get_json_text('base_order').format(
            order_id=order_id,
            user_id=user_id,
            game=product.game_name,
            category=product.category,
            product_name=product.name,
            product_price=product.price,
            login=order_data.additional_data.get('login'),
            password=order_data.additional_data.get('password'),
        )