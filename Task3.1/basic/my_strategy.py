import model
import random

max_health = 0

class MyStrategy:
    def __init__(self):
        pass

    def rrt(self, unit_pos, target_pos, unit, game):
        jump = False
        if unit_pos.y == target_pos.y:
            flag = 0
            if unit_pos.x > target_pos.x:
                for i in range(0,5):
                    if target_pos.x + i < 33 and game.level.tiles[int(target_pos.x + i)][int(target_pos.y)] == model.Tile.WALL:
                        flag = 1
                if flag == 0:
                    vel = target_pos.x - unit_pos.x
                    jump = False
                    return vel, jump
            elif unit_pos.x > target_pos.x:
                for i in range(0,5):
                    if target_pos.x - i > 0 and game.level.tiles[int(target_pos.x - i)][int(target_pos.y)] == model.Tile.WALL:
                        flag = 1
                if flag == 0:
                    vel = target_pos.x - unit_pos.x
                    jump = False
                    return vel, jump
        elif unit_pos.x == target_pos.x:
            if target_pos.y > unit_pos.y and target_pos.y - unit_pos < unit.jump_state.max_time * unit.jump_state.speed:
                flag = 0
                for i in range(unit_pos.y, target_pos.y):
                    if game.level.tiles[int(unit_pos.x, y)] == model.Tile.WALL:
                        flag = 1
                        break
                if flag == 0:
                    jump = True
                    vel = 0
                    return vel, jump
        #   Random point selection
        while True:
            temp_x = random.randint(1,33)
            temp_y = random.randint(1,26)
            if game.level.tiles[temp_x][temp_y] == model.Tile.WALL:
                continue
            break
        vel = temp_x - unit_pos.x
        if temp_y > unit_pos.y:
            jump = True
        return vel, jump
            
                    

    def get_action(self, unit, game, debug):
        global max_health

        if unit.health > max_health:
            max_health = unit.health
        mine = False
        weapon_change = False
        shoot_e = True
        target_pos = unit.position
        # max_health = model.Properties.unit_max_health

        #   Determining nearest entities to pickup

        def distance_sqr(a, b):
            return (a.x - b.x)**2 + (a.y - b.y)**2
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key = lambda u: distance_sqr(u.position, unit.position),
            default = None
        )
        nearest_weapon = min(
            filter(lambda box : isinstance(
                box.item, model.Item.Weapon), game.loot_boxes
            ),
            key = lambda box: distance_sqr(box.position, unit.position),
            default = None
        )
        nearest_mine = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Mine), game.loot_boxes
            ),
            key = lambda box: distance_sqr(box.position, unit.position),
            default = None
        )
        nearest_health = min(
            filter(lambda box: isinstance(
                box.item, model.Item.HealthPack), game.loot_boxes
            ),
            key = lambda box: distance_sqr(box.position, unit.position),
            default = None
        )
        
        if unit.weapon is None and nearest_weapon is not None:
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position

        if nearest_health is not None and unit.health <= max_health*0.7:
            target_pos = nearest_health.position

        aim = model.Vec2Double(0,0)

        if nearest_enemy is not None:
            aim = model.Vec2Double(
                nearest_enemy.position.x - unit.position.x,
                nearest_enemy.position.y - unit.position.y
            )
        if unit.weapon is not None and nearest_mine is not None:
            if distance_sqr(nearest_mine.position, unit.position) < 100:
                target_pos = nearest_mine.position
        
        if unit.weapon is not None and nearest_weapon is not None:
            if int(nearest_weapon.item.weapon_type) > int(unit.weapon.typ):
                target_pos = nearest_weapon.position
                weapon_change = True
        
        #   Steering
        
        vel, jump = self.rrt(unit.position, target_pos, unit, game)

        #   Basic properties

        if nearest_enemy is not None and unit.weapon is not None:
            if nearest_enemy.position.x < unit.position.x and model.game.tiles[int(unit.position.x-1), int(unit.position.y)] == model.Tile.WALL:
                shoot_e = False
            elif nearest_enemy.position.x > unit.position.x and model.game.tiles[int(unit.position.x+1), int(unit.position.y)] == model.Tile.WALL:
                shoot_e = False


        
        #   Printing entites

        debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        debug.draw(model.CustomData.Log("Current pos: {}".format(unit.position)))
        debug.draw(model.CustomData.Log("Opponent position: {}".format(nearest_enemy.position)))



        return model.UnitAction(
            velocity = vel,
            jump = jump,
            jump_down = not jump,
            aim = aim,
            shoot = shoot_e,
            reload = False,
            swap_weapon = weapon_change,
            plant_mine = mine
        )