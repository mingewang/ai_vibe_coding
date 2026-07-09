import pygame


class FixedTimestepLoop:
    def __init__(self, target_fps=60):
        self.target_dt = 1.0 / target_fps
        self.accumulator = 0.0
        self.clock = pygame.time.Clock()
        self.alpha = 0.0
        self.running = False
        self.paused = False

    def run(self, world, renderer):
        self.running = True
        while self.running:
            if self.paused:
                self.clock.tick()
                continue

            frame_dt = self.clock.tick() / 1000.0
            self.accumulator += frame_dt

            while self.accumulator >= self.target_dt:
                world.update(self.target_dt)
                self.accumulator -= self.target_dt

            self.alpha = self.accumulator / self.target_dt
            renderer.render(world, self.alpha)

    def stop(self):
        self.running = False
