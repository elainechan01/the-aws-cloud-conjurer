import pygame
import asyncio
import websockets
import json
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
instruction_font = pygame.font.Font(None, 36)  # Smaller font for instructions

# Player properties
player = {
    "position": [400, 300],
    "letter": None
}

def get_server_uri():
    while True:
        ip = input("Enter the EC2 instance IP address: ").strip()
        if ip:
            return f"ws://{ip}:8765"
        print("Please enter a valid IP address")

async def game_loop():
    uri = get_server_uri()
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to server")
            
            # Get initial letter assignment from server
            response = await websocket.recv()
            initial_state = json.loads(response)
            player["letter"] = initial_state["assigned_letter"]
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                if not running:
                    break

                # Handle player movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player["position"][0] = max(0, player["position"][0] - 5)
                if keys[pygame.K_RIGHT]:
                    player["position"][0] = min(800, player["position"][0] + 5)
                if keys[pygame.K_UP]:
                    player["position"][1] = max(0, player["position"][1] - 5)
                if keys[pygame.K_DOWN]:
                    player["position"][1] = min(600, player["position"][1] + 5)

                try:
                    # Send player state to server
                    await websocket.send(json.dumps(player))
                    
                    # Receive game state from server
                    response = await websocket.recv()
                    game_state = json.loads(response)

                    # Clear screen
                    screen.fill((0, 0, 0))
                    
                    # Draw instruction text in the middle of the screen
                    instruction_text = instruction_font.render("Use arrow keys to move", True, (128, 128, 128))
                    instruction_rect = instruction_text.get_rect(center=(400, 300))
                    screen.blit(instruction_text, instruction_rect)
                    
                    # Draw all players as letters
                    for player_data in game_state["players"].values():
                        pos = player_data["position"]
                        letter = player_data["letter"]
                        text = font.render(letter, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(int(pos[0]), int(pos[1])))
                        screen.blit(text, text_rect)

                    pygame.display.flip()
                    await asyncio.sleep(0.016)

                except websockets.exceptions.ConnectionClosed:
                    print("Server connection closed")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

    except ConnectionRefusedError:
        print(f"Could not connect to server at {uri}")
        print("Please check the IP address and ensure the server is running")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        asyncio.run(game_loop())
    except KeyboardInterrupt:
        print("Game terminated by user")
    except Exception as e:
        print(f"Game crashed: {e}")
    finally:
        pygame.quit()
        sys.exit()
