# src/main.py

import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui import MainWindow
from screen_reader import ScreenCapture
from utils import GemDetector
from game_logic import MoveFinder, BoardState
from config import Config

class DragonChessAssistant:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        self.screen_capture = ScreenCapture(
            x=Config.GRID_START_X,
            y=Config.GRID_START_Y,
            width=Config.GRID_SIZE * Config.BOX_SIZE,
            height=Config.GRID_SIZE * Config.BOX_SIZE
        )
        self.gem_detector = GemDetector()
        self.board_state = BoardState(rows=Config.GRID_SIZE, cols=Config.GRID_SIZE)
        self.move_finder = MoveFinder(rows=Config.GRID_SIZE, cols=Config.GRID_SIZE)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def start(self):
        self.window.show()
        self.timer.start(int(Config.CHECK_INTERVAL * 1000))  # Convert to milliseconds
        return self.app.exec()

    def update(self):
        if self.window.assistant_active:
            grid = self.screen_capture.get_grid(rows=Config.GRID_SIZE, cols=Config.GRID_SIZE)
            gem_grid = self.gem_detector.process_grid(grid)
            self.board_state.update_grid(gem_grid)
            moves = self.move_finder.find_moves(self.board_state.grid)
            self.window.overlay.update_moves(moves)
            
            if self.window.debug_active:
                self.window.debug_window.update_grid(gem_grid)
            
            logging.debug(f"Current board state:\n{self.board_state}")
            logging.debug(f"Possible moves: {moves}")

def main():
    logging.basicConfig(level=logging.DEBUG)
    assistant = DragonChessAssistant()
    assistant.start()

if __name__ == "__main__":
    main()