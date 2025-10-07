import pygame
import sys
import math

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
TILE_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 40)
WALL_COLOR = (52, 73, 94)
FLOOR_COLOR = (236, 240, 241)
PLAYER_COLOR = (46, 204, 113)
BOX_COLOR = (230, 126, 34)
WEB2_COLOR = (231, 76, 60)
WEB3_COLOR = (52, 152, 219)
WEB2_GLOW = (255, 200, 200)
WEB3_GLOW = (200, 230, 255)
BOX_ON_TARGET = (241, 196, 15)
SHADOW_COLOR = (0, 0, 0, 50)
TEXT_COLOR = (44, 62, 80)
LIGHT_TEXT = (149, 165, 166)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SokobanGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Sokoban: Web2 to Web3 Journey')
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.SysFont('segoeui', 48, bold=True)
        self.font = pygame.font.SysFont('segoeui', 22, bold=True)
        self.small_font = pygame.font.SysFont('segoeui', 16)
        self.tiny_font = pygame.font.SysFont('segoeui', 12)
        
        self.level = 0
        self.moves = 0
        self.pushes = 0
        self.history = []
        self.levels = self.create_levels()
        
        # Animation states
        self.animating = False
        self.anim_direction = None
        self.anim_progress = 0
        self.anim_speed = 0.25
        
        # Transition animation
        self.transitioning = False
        self.transition_progress = 0
        self.transition_speed = 0.02
        
        # Particle effects
        self.particles = []
        
        self.load_level(self.level)
        self.player_image = pygame.image.load("image-removebg-preview.png").convert_alpha()
        self.player_image = pygame.transform.smoothscale(self.player_image, (TILE_SIZE, TILE_SIZE))

        
    def create_levels(self):
        """Create challenging Sokoban levels - increasing difficulty"""
        return [
            # Level 1: Learn the basics - simple corridor
            {
                'map': [
                    "##############",
                    "##           #",
                    "# P$         #",
                    "#            #",
                    "#   ######   #",
                    "#            #",
                    "#   ######   #",
                    "#            #",
                    "#          .W#",
                    "##############"
                ],
                'name': 'First Push',
                'description': 'Learn to push the box'
            },
            # Level 2: First puzzle - can't push straight
            {
                'map': [
                    "###############",
                    "##            #",
                    "# P$          #",
                    "#       ##### #",
                    "#       #     #",
                    "#  ######  ####",
                    "#             #",
                    "#  #########  #",
                    "#           .W#",
                    "###############"
                ],
                'name': 'Detour',
                'description': 'Find another way'
            },
            # Level 3: Dead end trap - must avoid corner
            {
                'map': [
                    "################",
                    "##             #",
                    "# P$    ####   #",
                    "#       #      #",
                    "#  ######   ####",
                    "#           #  #",
                    "#  ######   #  #",
                    "#       #      #",
                    "#  #####    # .#",
                    "#           # W#",
                    "################"
                ],
                'name': 'Dead End',
                'description': 'Avoid the corners!'
            },
            # Level 4: U-turn puzzle
            {
                'map': [
                    "#################",
                    "##              #",
                    "# P$            #",
                    "#  ############ #",
                    "#            #  #",
                    "############ #  #",
                    "#               #",
                    "#  ###########  #",
                    "#             # #",
                    "#  #########  #.#",
                    "#          #  #W#",
                    "#################"
                ],
                'name': 'U-Turn',
                'description': 'Master the turns'
            },
            # Level 5: Narrow corridor with obstacles
            {
                'map': [
                    "##################",
                    "##               #",
                    "# P$       ##### #",
                    "#   ####       # #",
                    "# #    # ##### # #",
                    "# # ##       # # #",
                    "# # #  ##### #   #",
                    "# #       #  # # #",
                    "#   ##### # ## # #",
                    "# #     # #    #.#",
                    "# ##### # #### #W#",
                    "##################"
                ],
                'name': 'Labyrinth',
                'description': 'Navigate carefully'
            },
            # Level 6: Multiple dead ends - high difficulty
            {
                'map': [
                    "#####################",
                    "##                  #",
                    "# P$   #####   #### #",
                    "#   # #    #      # #",
                    "# # # # ## # #### # #",
                    "# # #   #  #    # # #",
                    "# # ##### ## ## # # #",
                    "# #       #  #  #   #",
                    "# ####### # ## #### #",
                    "#         #       #.#",
                    "#  ############## #W#",
                    "#####################"
                ],
                'name': 'The Gauntlet',
                'description': 'Think 10 steps ahead'
            },
            # Level 7: MASTER LEVEL - extremely difficult
            {
                'map': [
                    "########################",
                    "##                     #",
                    "# P$    ####   ####    #",
                    "#    # #   # #    #    #",
                    "# ## # # # # # ## # ####",
                    "# #  #   # # #  # #    #",
                    "# # ##### # #### # ##  #",
                    "# #     # #    #     # #",
                    "# ##### # #### ##### # #",
                    "#     # #    #     # # #",
                    "# ### # #### # ### # # #",
                    "#   #        #   # #  .#",
                    "# # ############ # # #W#",
                    "########################"
                ],
                'name': 'NIGHTMARE',
                'description': 'Only for masters!'
            }
        ]
    
    def load_level(self, level_index):
        """Load a level"""
        if level_index >= len(self.levels):
            return False
            
        level_data = self.levels[level_index]
        self.current_map = level_data['map']
        self.level_name = level_data['name']
        self.level_description = level_data['description']
        
        # Parse map
        self.walls = set()
        self.floor = set()
        
        for y, row in enumerate(self.current_map):
            for x, cell in enumerate(row):
                pos = (x, y)
                if cell == '#':
                    self.walls.add(pos)
                elif cell == 'P':
                    self.player_pos = list(pos)
                    self.floor.add(pos)
                elif cell == '$':
                    self.box_pos = list(pos)
                    self.floor.add(pos)
                elif cell == '.':
                    self.target_pos = pos
                    self.floor.add(pos)
                elif cell == 'W':
                    self.web3_pos = pos
                    self.floor.add(pos)
                elif cell == ' ':
                    self.floor.add(pos)
        
        # Calculate offset to center the level
        self.map_width = max(len(row) for row in self.current_map)
        self.map_height = len(self.current_map)
        self.offset_x = (SCREEN_WIDTH - self.map_width * TILE_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - self.map_height * TILE_SIZE) // 2 + 30
        
        self.moves = 0
        self.pushes = 0
        self.history = []
        self.box_on_target = False
        self.particles = []
        return True
    
    def to_screen_pos(self, grid_pos):
        """Convert grid position to screen coordinates"""
        return (
            grid_pos[0] * TILE_SIZE + self.offset_x,
            grid_pos[1] * TILE_SIZE + self.offset_y
        )
    
    def is_valid_move(self, pos):
        """Check if position is valid"""
        return tuple(pos) not in self.walls and tuple(pos) in self.floor
    
    def move_player(self, direction):
        """Move player and handle box pushing"""
        if self.animating or self.transitioning:
            return
            
        new_pos = [
            self.player_pos[0] + direction[0],
            self.player_pos[1] + direction[1]
        ]
        
        # Save state for undo
        old_state = {
            'player': self.player_pos[:],
            'box': self.box_pos[:],
            'moves': self.moves,
            'pushes': self.pushes,
            'box_on_target': self.box_on_target
        }
        
        # Check if there's the box
        if new_pos == self.box_pos:
            box_new_pos = [
                self.box_pos[0] + direction[0],
                self.box_pos[1] + direction[1]
            ]
            
            # Check if we can push the box
            if self.is_valid_move(box_new_pos):
                self.box_pos = box_new_pos
                self.player_pos = new_pos
                self.pushes += 1
                self.moves += 1
                self.history.append(old_state)
                self.start_animation(direction)
                
                # Check if box is on target
                if tuple(self.box_pos) == self.target_pos:
                    self.box_on_target = True
                    self.create_success_particles()
                    self.start_transition()
                else:
                    self.box_on_target = False
                
                # Check win condition immediately after pushing
                if self.box_on_target and tuple(self.player_pos) == self.target_pos:
                    self.start_transition()
        elif self.is_valid_move(new_pos):
            self.player_pos = new_pos
            self.moves += 1
            self.history.append(old_state)
            self.start_animation(direction)
        
        # Check if player reached target when box is on target (check after any move)
        if self.box_on_target and tuple(self.player_pos) == self.target_pos:
            self.start_transition()
    
    def start_animation(self, direction):
        """Start movement animation"""
        self.animating = True
        self.anim_direction = direction
        self.anim_progress = 0
    
    def update_animation(self):
        """Update animation"""
        if self.animating:
            self.anim_progress += self.anim_speed
            if self.anim_progress >= 1.0:
                self.animating = False
                self.anim_progress = 0
    
    def start_transition(self):
        """Start level transition"""
        self.transitioning = True
        self.transition_progress = 0
        self.create_transition_particles()
    
    def update_transition(self):
        """Update transition animation"""
        if self.transitioning:
            self.transition_progress += self.transition_speed
            if self.transition_progress >= 1.0:
                self.transitioning = False
                self.transition_progress = 0
                self.level += 1
                if not self.load_level(self.level):
                    # All levels complete
                    self.level = len(self.levels)
    
    def create_success_particles(self):
        """Create particles when box reaches target"""
        screen_pos = self.to_screen_pos(self.target_pos)
        center = (screen_pos[0] + TILE_SIZE // 2, screen_pos[1] + TILE_SIZE // 2)
        for _ in range(30):
            angle = math.radians(360 * _ / 30)
            speed = 2 + (_ % 3)
            self.particles.append({
                'pos': list(center),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': 60,
                'color': BOX_ON_TARGET
            })
    
    def create_transition_particles(self):
        """Create particles for level transition"""
        screen_pos = self.to_screen_pos(self.web3_pos)
        center = (screen_pos[0] + TILE_SIZE // 2, screen_pos[1] + TILE_SIZE // 2)
        for _ in range(50):
            angle = math.radians(360 * _ / 50)
            speed = 3 + (_ % 4)
            self.particles.append({
                'pos': list(center),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': 80,
                'color': WEB3_COLOR
            })
    
    def update_particles(self):
        """Update particle positions"""
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def undo_move(self):
        """Undo last move"""
        if self.history and not self.transitioning:
            state = self.history.pop()
            self.player_pos = state['player']
            self.box_pos = state['box']
            self.moves = state['moves']
            self.pushes = state['pushes']
            self.box_on_target = state['box_on_target']
    
    def draw_glow(self, pos, color, radius=40):
        """Draw glowing effect"""
        screen_pos = self.to_screen_pos(pos)
        center = (screen_pos[0] + TILE_SIZE // 2, screen_pos[1] + TILE_SIZE // 2)
        
        for i in range(3):
            alpha = 30 - i * 10
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            glow_color = (*color[:3], alpha)
            pygame.draw.circle(glow_surface, glow_color, (radius, radius), radius - i * 10)
            self.screen.blit(glow_surface, (center[0] - radius, center[1] - radius))
    
    def draw_rialo_logo(self, surface, center_x, center_y, size):
        """Draw accurate Rialo logo based on the provided image"""
        scale = size / 35
        
        # Create temporary surface for the logo
        logo_size = int(size * 2.5)
        logo_surf = pygame.Surface((logo_size, logo_size), pygame.SRCALPHA)
        cx, cy = logo_size // 2, logo_size // 2
        
        # Top horizontal bar with rounded ends
        top_bar = pygame.Rect(cx - 20 * scale, cy - 18 * scale,
                             28 * scale, 10 * scale)
        pygame.draw.rect(logo_surf, BLACK, top_bar, border_radius=int(5 * scale))
        
        # Top right bulge (rounded)
        pygame.draw.circle(logo_surf, BLACK,
                         (int(cx + 13 * scale), int(cy - 13 * scale)),
                         int(9 * scale))
        
        # Middle horizontal bar (left side)
        mid_left_bar = pygame.Rect(cx - 20 * scale, cy - 4 * scale,
                                   20 * scale, 10 * scale)
        pygame.draw.rect(logo_surf, BLACK, mid_left_bar, border_radius=int(5 * scale))
        
        # Middle right connection (curves into the leg)
        mid_right = pygame.Rect(cx, cy - 4 * scale,
                               10 * scale, 10 * scale)
        pygame.draw.rect(logo_surf, BLACK, mid_right, border_radius=int(5 * scale))
        
        # White circle cutout in the middle (the hole)
        pygame.draw.circle(logo_surf, (0, 0, 0, 0),
                         (int(cx + 7 * scale), int(cy + 1 * scale)),
                         int(7.5 * scale))
        
        # Right curved bulge connecting to leg
        pygame.draw.circle(logo_surf, BLACK,
                         (int(cx + 7 * scale), int(cy + 8 * scale)),
                         int(10 * scale))
        
        # Vertical leg (right side, going down)
        leg = pygame.Rect(cx + 2 * scale, cy + 8 * scale,
                         10 * scale, 18 * scale)
        pygame.draw.rect(logo_surf, BLACK, leg, border_radius=int(5 * scale))
        
        # Bottom rounded cap
        pygame.draw.circle(logo_surf, BLACK,
                         (int(cx + 7 * scale), int(cy + 26 * scale)),
                         int(5 * scale))
        
        # Left rounded cap (top bar)
        pygame.draw.circle(logo_surf, BLACK,
                         (int(cx - 20 * scale), int(cy - 13 * scale)),
                         int(5 * scale))
        
        # Left rounded cap (middle bar)
        pygame.draw.circle(logo_surf, BLACK,
                         (int(cx - 20 * scale), int(cy + 1 * scale)),
                         int(5 * scale))
        
        # Blit to main surface
        logo_pos = (int(center_x - logo_size // 2), int(center_y - logo_size // 2))
        surface.blit(logo_surf, logo_pos)
    
    def draw_player(self):
        """Draw player with custom image"""
        pos = self.player_pos
        if self.animating:
            offset_x = -self.anim_direction[0] * TILE_SIZE * (1 - self.anim_progress)
            offset_y = -self.anim_direction[1] * TILE_SIZE * (1 - self.anim_progress)
        else:
            offset_x = offset_y = 0

        screen_pos = self.to_screen_pos(pos)
        screen_pos = (screen_pos[0] + offset_x, screen_pos[1] + offset_y)

        # Shadow
        shadow_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 60),
                        (TILE_SIZE // 2 + 3, TILE_SIZE // 2 + 3),
                        TILE_SIZE // 3 + 3)
        self.screen.blit(shadow_surf, screen_pos)

        # Draw the custom player image
        self.screen.blit(self.player_image, screen_pos)

    
    def draw_box(self):
        """Draw box with animation"""
        pos = self.box_pos
        if self.animating and self.history and self.history[-1]['box'] != self.box_pos:
            offset_x = -self.anim_direction[0] * TILE_SIZE * (1 - self.anim_progress)
            offset_y = -self.anim_direction[1] * TILE_SIZE * (1 - self.anim_progress)
        else:
            offset_x = offset_y = 0
        
        screen_pos = self.to_screen_pos(pos)
        screen_pos = (screen_pos[0] + offset_x, screen_pos[1] + offset_y)
        
        # Shadow
        shadow_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, SHADOW_COLOR, 
                       (4, 4, TILE_SIZE - 8, TILE_SIZE - 8), 
                       border_radius=10)
        self.screen.blit(shadow_surf, screen_pos)
        
        # Box color based on state
        if self.box_on_target:
            color = BOX_ON_TARGET
            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() / 300))
            self.draw_glow(pos, color, int(50 + pulse * 20))
        else:
            color = BOX_COLOR
        
        # Box
        rect = pygame.Rect(screen_pos[0] + 4, screen_pos[1] + 4, 
                         TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        # Box details
        inner_rect = pygame.Rect(screen_pos[0] + 10, screen_pos[1] + 10,
                                TILE_SIZE - 20, TILE_SIZE - 20)
        lighter = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(self.screen, lighter, inner_rect, border_radius=6)
        
        # Border
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(FLOOR_COLOR)
        
        # Draw floor with gradient
        for pos in self.floor:
            screen_pos = self.to_screen_pos(pos)
            rect = pygame.Rect(screen_pos[0] + 3, screen_pos[1] + 3, 
                             TILE_SIZE - 6, TILE_SIZE - 6)
            
            # Subtle checkerboard
            if (pos[0] + pos[1]) % 2 == 0:
                color = (245, 245, 250)
            else:
                color = WHITE
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
        
        # Draw Web2 area (top-left) with glow
        web2_pos = (self.player_pos[0] if self.moves == 0 else 0, 
                    self.player_pos[1] if self.moves == 0 else 0)
        self.draw_glow(web2_pos, WEB2_COLOR, 60)
        
        # Draw Web3 target with animated glow
        pulse = abs(math.sin(pygame.time.get_ticks() / 500))
        self.draw_glow(self.web3_pos, WEB3_COLOR, int(70 + pulse * 30))
        
        screen_pos = self.to_screen_pos(self.target_pos)
        center = (screen_pos[0] + TILE_SIZE // 2, screen_pos[1] + TILE_SIZE // 2)
        
        # Target rings
        for i in range(3):
            radius = TILE_SIZE // 3 + i * 5
            width = 3 if i == 1 else 2
            color = WEB3_COLOR if not self.box_on_target else BOX_ON_TARGET
            pygame.draw.circle(self.screen, color, center, radius, width)
        
        # Draw walls with 3D effect
        for pos in self.walls:
            screen_pos = self.to_screen_pos(pos)
            
            # Main wall
            rect = pygame.Rect(screen_pos[0], screen_pos[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=4)
            
            # Top highlight
            highlight_rect = pygame.Rect(screen_pos[0] + 4, screen_pos[1] + 4,
                                        TILE_SIZE - 8, 6)
            pygame.draw.rect(self.screen, (70, 90, 110), highlight_rect, border_radius=2)
            
            # Side shadow
            shadow_rect = pygame.Rect(screen_pos[0] + 4, screen_pos[1] + TILE_SIZE - 10,
                                     TILE_SIZE - 8, 6)
            pygame.draw.rect(self.screen, (30, 40, 50), shadow_rect, border_radius=2)
        
        # Draw labels
        # Web2 label
        web2_text = self.font.render('WEB2', True, WEB2_COLOR)
        web2_bg = pygame.Surface((web2_text.get_width() + 20, web2_text.get_height() + 10), 
                                 pygame.SRCALPHA)
        web2_bg.fill((*WHITE, 230))
        start_screen_pos = self.to_screen_pos((0, 0))
        self.screen.blit(web2_bg, (start_screen_pos[0] + 5, start_screen_pos[1] + 5))
        self.screen.blit(web2_text, (start_screen_pos[0] + 15, start_screen_pos[1] + 10))
        
        # Web3 label
        web3_text = self.font.render('WEB3', True, WEB3_COLOR)
        web3_bg = pygame.Surface((web3_text.get_width() + 20, web3_text.get_height() + 10),
                                 pygame.SRCALPHA)
        web3_bg.fill((*WHITE, 230))
        end_screen_pos = self.to_screen_pos(self.web3_pos)
        self.screen.blit(web3_bg, (end_screen_pos[0] + 5, end_screen_pos[1] + 5))
        self.screen.blit(web3_text, (end_screen_pos[0] + 15, end_screen_pos[1] + 10))
        
        # Draw box and player
        self.draw_box()
        self.draw_player()
        
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 80))
            size = max(2, int(6 * (particle['life'] / 80)))
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(particle_surf, color, (size, size), size)
            self.screen.blit(particle_surf, (particle['pos'][0] - size, particle['pos'][1] - size))
        
        # Draw UI
        self.draw_ui()
        
        # Draw transition overlay
        if self.transitioning:
            self.draw_transition()
    
    def draw_ui(self):
        """Draw UI elements"""
        # Top bar
        top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(self.screen, BLACK, top_bar)
        
        # Title with gradient effect
        title = self.title_font.render('Web2 → Web3 Journey', True, WHITE)
        self.screen.blit(title, (20, 12))
        
        # Level info
        level_text = self.font.render(
            f'Level {self.level + 1}/{len(self.levels)}: {self.level_name}', 
            True, WEB3_COLOR
        )
        self.screen.blit(level_text, (20, 45))
        
        # Stats
        moves_text = self.small_font.render(f'Moves: {self.moves}', True, WHITE)
        pushes_text = self.small_font.render(f'Pushes: {self.pushes}', True, WHITE)
        self.screen.blit(moves_text, (SCREEN_WIDTH - 200, 18))
        self.screen.blit(pushes_text, (SCREEN_WIDTH - 200, 42))
        
        # Objective indicator
        if self.box_on_target:
            obj_text = self.small_font.render('✓ Box placed! Now step on target to advance!', 
                                            True, BOX_ON_TARGET)
        else:
            obj_text = self.small_font.render('Push box to the target (circle)', True, LIGHT_TEXT)
        obj_x = SCREEN_WIDTH // 2 - obj_text.get_width() // 2
        self.screen.blit(obj_text, (obj_x, SCREEN_HEIGHT - 60))
        
        # Bottom bar
        bottom_bar = pygame.Rect(0, SCREEN_HEIGHT - 35, SCREEN_WIDTH, 35)
        pygame.draw.rect(self.screen, BLACK, bottom_bar)
        
        # Controls
        controls = self.tiny_font.render(
            'Arrow Keys: Move  |  U: Undo  |  R: Restart',
            True, LIGHT_TEXT
        )
        self.screen.blit(controls, (20, SCREEN_HEIGHT - 24))
        
        # Credits
        credit = self.tiny_font.render(
            'Say Hello to Rialo. Designed by Kharather',
            True, LIGHT_TEXT
        )
        credit_x = SCREEN_WIDTH - credit.get_width() - 20
        self.screen.blit(credit, (credit_x, SCREEN_HEIGHT - 24))
    
    def draw_transition(self):
        """Draw level transition animation"""
        # Fade out
        alpha = int(255 * self.transition_progress)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, alpha))
        self.screen.blit(overlay, (0, 0))
        
        # Success message
        if self.transition_progress > 0.3:
            progress = (self.transition_progress - 0.3) / 0.7
            scale = min(1.0, progress * 2)
            
            if self.level < len(self.levels):
                text = self.title_font.render('Level Complete!', True, WEB3_COLOR)
            else:
                text = self.title_font.render('All Levels Complete!', True, BOX_ON_TARGET)
            
            # Scale text
            scaled_width = int(text.get_width() * scale)
            scaled_height = int(text.get_height() * scale)
            if scaled_width > 0 and scaled_height > 0:
                scaled_text = pygame.transform.scale(text, (scaled_width, scaled_height))
                text_x = SCREEN_WIDTH // 2 - scaled_width // 2
                text_y = SCREEN_HEIGHT // 2 - scaled_height // 2
                self.screen.blit(scaled_text, (text_x, text_y))
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.transitioning:
                    if event.key == pygame.K_UP:
                        self.move_player(UP)
                        self.last_direction = UP
                    elif event.key == pygame.K_DOWN:
                        self.move_player(DOWN)
                        self.last_direction = DOWN
                    elif event.key == pygame.K_LEFT:
                        self.move_player(LEFT)
                        self.last_direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.move_player(RIGHT)
                        self.last_direction = RIGHT
                    elif event.key == pygame.K_u:
                        self.undo_move()
                    elif event.key == pygame.K_r:
                        self.load_level(self.level)
            
            self.update_animation()
            self.update_transition()
            self.update_particles()
            
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == '__main__':
    game = SokobanGame()
    game.run()
