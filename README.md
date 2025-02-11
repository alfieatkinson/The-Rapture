# The Rapture

This game was developed for my **A-Level Computer Science NEA (Non-Exam Assessment)**, achieving an A*.

## Features

- **Player Control**: Move the player using `A` and `D` keys, jump with `SPACE`, and shoot with the mouse.
- **Enemies**: Two types of enemies - Walking Demons and Flying Demons, each with unique behaviors and attributes.
- **Platforms**: Randomly generated platforms to navigate through the game.
- **Health and Score**: Displayed on the screen with a health bar and score counter.
- **Game Over**: The game ends when the player's health reaches zero.
- **Save and Load**: Save and load game states using pickle files.
- **Menu System**: Navigate through the main menu and pause menu with options to start, load, save, and quit the game.

## Installation

1. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

2. Run the game:

    ```sh
    python main.py
    ```

## Controls

- **Move Left**: `A`
- **Move Right**: `D`
- **Jump**: `SPACE`
- **Shoot**: Mouse click

## Classes

### `entities.py`

- **`Player`**: Represents the player character. Handles movement, jumping, shooting, and collision detection.
- **`Platform`**: Represents platforms in the game. Handles platform creation and collision detection.
- **`Enemy`**: Base class for enemies. Handles enemy attributes and behaviors.
  - **`WalkingDemon`**: Inherits from `Enemy`. Represents a walking demon with specific movement and attack patterns.
  - **`FlyingDemon`**: Inherits from `Enemy`. Represents a flying demon with specific movement and attack patterns.
- **`Bullet`**: Represents bullets fired by the player. Handles bullet movement and collision with enemies.

### `gui.py`

- **`HPBar`**: Displays the player's health bar.
- **`Score`**: Displays the player's score.
- **`Button`**: Represents a button in the menu system. Handles button rendering and interaction.
- **`alert`**: Displays an alert message using Tkinter.
- **`confirm`**: Displays a confirmation dialog using Tkinter.

### `gamesystem.py`

- **`Game`**: Manages the game state, including player, platforms, enemies, bullets, and GUI elements. Handles game updates, platform and enemy generation, and game over conditions.
- **`Menu`**: Manages the main menu and pause menu. Handles menu navigation and interaction.