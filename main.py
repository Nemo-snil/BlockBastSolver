import copy

import util

block_bast_map = util.get_map()

block_bast_items = []
for _ in range(3):
    item = util.get_map(True)
    if item == 0:
        break
    else:
        block_bast_items.append(item)


util.block_bast_items_transformation(block_bast_items)


def block_bast_solve(new_block_bast_map, new_block_bast_items, steps=[]):
    new_steps = copy.deepcopy(steps)

    new_block_bast_item = new_block_bast_items[0]

    item_width = len(new_block_bast_item[0])
    item_height = len(new_block_bast_item)

    map_width = len(new_block_bast_map[0])
    map_height = len(new_block_bast_map)

    for y_offset in range(0, map_height - item_height + 1):
        for x_offset in range(0, map_width - item_width + 1):
            new_steps = copy.deepcopy(steps)
            plus_array = util.plus_array(new_block_bast_item,
                                         util.cut_array(new_block_bast_map, x_offset, x_offset + item_width, y_offset,
                                                        y_offset + item_height))
            for array in plus_array:
                if 5 in array or 8 in array:
                    break
            else:
                new_steps.append(util.paste_array(plus_array, new_block_bast_map, x_offset, y_offset))
                if len(new_block_bast_items) == 1:
                    return new_steps
                else:
                    out = block_bast_solve(
                        util.clean_map(util.paste_array(plus_array, new_block_bast_map, x_offset, y_offset)),
                        new_block_bast_items[1:], new_steps)
                    if out != 0:
                        return out

    return 0


def get_solve(block_bast_map, block_bast_items):
    out = block_bast_solve(block_bast_map, block_bast_items)
    if out != 0:
        return out

    out = block_bast_solve(block_bast_map, [block_bast_items[0], block_bast_items[2], block_bast_items[1]])
    if out != 0:
        return out

    out = block_bast_solve(block_bast_map, [block_bast_items[1], block_bast_items[0], block_bast_items[2]])
    if out != 0:
        return out

    out = block_bast_solve(block_bast_map, [block_bast_items[1], block_bast_items[2], block_bast_items[0]])
    if out != 0:
        return out

    out = block_bast_solve(block_bast_map, [block_bast_items[2], block_bast_items[0], block_bast_items[1]])
    if out != 0:
        return out

    out = block_bast_solve(block_bast_map, [block_bast_items[2], block_bast_items[1], block_bast_items[0]])
    if out != 0:
        return out

    return 0


out = get_solve(block_bast_map, block_bast_items)
if out != 0:
    util.draw_images(out)
    print("Сосать нахуй")
else:
    print("Пизда бля")
