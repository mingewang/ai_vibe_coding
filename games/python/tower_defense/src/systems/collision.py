import math


def circle_circle(ax, ay, ar, bx, by, br):
    dx = bx - ax
    dy = by - ay
    dist_sq = dx * dx + dy * dy
    return dist_sq <= (ar + br) * (ar + br)


def circle_point(cx, cy, cr, px, py):
    dx = px - cx
    dy = py - cy
    return dx * dx + dy * dy <= cr * cr


def aabb_aabb(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def resolve_projectile_enemy(projectile, enemy):
    if not projectile.active or not enemy.active:
        return False
    if id(enemy) in projectile.hit_enemies:
        return False
    if circle_circle(projectile.x, projectile.y, projectile.radius,
                     enemy.center_x, enemy.center_y, enemy.radius):
        projectile.hit_enemies.add(id(enemy))
        enemy.take_damage(projectile.damage)

        if projectile.splash_radius > 0:
            return "splash"

        if projectile.slow_duration > 0:
            enemy.apply_slow(projectile.slow_duration, projectile.slow_multiplier)

        if projectile.pierce > 0:
            projectile.pierce -= 1
            if projectile.pierce <= 0:
                projectile.active = False
        else:
            projectile.active = False

        return True
    return False


def get_enemies_in_radius(cx, cy, radius, enemies):
    hit = []
    r_sq = radius * radius
    for e in enemies:
        if not e.active:
            continue
        dx = cx - e.center_x
        dy = cy - e.center_y
        if dx * dx + dy * dy <= r_sq:
            hit.append(e)
    return hit
