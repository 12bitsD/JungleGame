"""
Game Controller for Jungle Game.
Handles game logic coordination between model and view.
"""

from model import GameState, MoveValidator, GameStatus
from view.cli_view import CLIView
from view.replay_engine import ReplayEngine


class GameController:
    """
    Main game controller.
    Coordinates between game state (model) and display (view).
    """
    
    def __init__(self):
        self.game_state = GameState()
        self.view = CLIView()
    
    def start(self):
        """Start the game loop."""
        self.view.display_menu()
        
        if self.view.confirm_action("Start a new game?"):
            self.game_state.start_new_game()
            self.view.display_success("New game started!")
        
        self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        while True:
            # Display current state
            self.view.display_board(self.game_state.board)
            self.view.display_game_status(self.game_state)
            
            # Check if game is over
            if self.game_state.game_status != GameStatus.IN_PROGRESS:
                self.view.display_game_over(
                    self.game_state.game_status,
                    self.game_state
                )
                
                if self.view.confirm_action("Start a new game?"):
                    self.game_state.start_new_game()
                    continue
                else:
                    break
            
            # Get user command
            command = self.view.get_user_input("\nEnter command: ").lower()
            
            if not command:
                continue
            
            # Parse and execute command
            self.handle_command(command)
    
    def handle_command(self, command: str):
        """Parse and execute user command."""
        parts = command.split()
        cmd = parts[0]
        
        if cmd == "move" and len(parts) == 3:
            self.handle_move(parts[1], parts[2])
        
        elif cmd == "show" and len(parts) == 2:
            self.handle_show_moves(parts[1])
        
        elif cmd == "undo":
            self.handle_undo()
        
        elif cmd == "redo":
            self.handle_redo()
        
        elif cmd == "history":
            self.handle_history()
        
        elif cmd == "save" and len(parts) == 2:
            self.handle_save(parts[1])
        
        elif cmd == "load" and len(parts) == 2:
            self.handle_load(parts[1])
        
        elif cmd == "new":
            self.handle_new_game()
        
        elif cmd == "replay":
            self.handle_replay()
        
        elif cmd == "quit":
            if self.view.confirm_action("Are you sure you want to quit?"):
                self.view.display_message("Thanks for playing!")
                exit(0)
        
        else:
            self.view.display_error("Invalid command. Type 'help' for available commands.")
    
    def handle_move(self, from_pos: str, to_pos: str):
        """Handle move command."""
        try:
            from_row, from_col = self.game_state.board.notation_to_position(from_pos)
            to_row, to_col = self.game_state.board.notation_to_position(to_pos)
            
            success, message = self.game_state.make_move(from_row, from_col, to_row, to_col)
            
            if success:
                self.view.display_success(message)
            else:
                self.view.display_error(message)
        
        except (ValueError, IndexError):
            self.view.display_error("Invalid position format. Use format like 'E3'")
    
    def handle_show_moves(self, pos: str):
        """Show legal moves for piece at position."""
        try:
            row, col = self.game_state.board.notation_to_position(pos)
            piece = self.game_state.board.get_piece(row, col)
            
            if not piece:
                self.view.display_error("No piece at that position")
                return
            
            if piece.owner != self.game_state.current_player:
                self.view.display_error("That's not your piece")
                return
            
            validator = MoveValidator(self.game_state.board)
            legal_moves = validator.get_legal_moves(piece)
            
            # Display board with highlighted legal moves
            self.view.display_board(self.game_state.board, legal_moves)
            self.view.display_legal_moves(self.game_state.board, piece, legal_moves)
        
        except (ValueError, IndexError):
            self.view.display_error("Invalid position format. Use format like 'E3'")
    
    def handle_undo(self):
        """Handle undo command."""
        success, message = self.game_state.undo()
        if success:
            self.view.display_success(message)
        else:
            self.view.display_error(message)
    
    def handle_redo(self):
        """Handle redo command."""
        success, message = self.game_state.redo()
        if success:
            self.view.display_success(message)
        else:
            self.view.display_error(message)
    
    def handle_history(self):
        """Handle history command."""
        self.view.display_move_history(self.game_state)
    
    def handle_save(self, filename: str):
        """Handle save command."""
        if not filename.endswith('.json'):
            filename += '.json'
        
        success, message = self.game_state.save_to_file(filename)
        if success:
            self.view.display_success(message)
        else:
            self.view.display_error(message)
    
    def handle_load(self, filename: str):
        """Handle load command."""
        if not filename.endswith('.json'):
            filename += '.json'
        
        success, message = self.game_state.load_from_file(filename)
        if success:
            self.view.display_success(message)
        else:
            self.view.display_error(message)
    
    def handle_new_game(self):
        """Handle new game command."""
        if self.view.confirm_action("Start a new game? Current game will be lost if not saved."):
            self.game_state.start_new_game()
            self.view.display_success("New game started!")
    
    def handle_replay(self):
        """Handle replay command."""
        if not self.game_state.move_history:
            self.view.display_error("No moves to replay")
            return
        
        self.replay_mode()
    
    def replay_mode(self):
        """Enter replay mode."""
        engine = ReplayEngine(self.game_state)
        self.view.display_replay_controls()
        
        while True:
            self.view.display_board(engine.board)
            
            current, total = engine.get_progress()
            print(f"\nReplay Progress: {current}/{total}")
            
            if current > 0:
                move = engine.get_current_move()
                if move:
                    print(f"Last move: {move.to_notation(self.game_state.board)}")
            
            command = self.view.get_user_input("\nReplay command: ").lower().split()
            
            if not command:
                continue
            
            cmd = command[0]
            
            if cmd in ('next', 'n'):
                if not engine.step_forward():
                    self.view.display_message("Already at end of game")
            
            elif cmd in ('prev', 'p'):
                if not engine.step_backward():
                    self.view.display_message("Already at start of game")
            
            elif cmd == 'goto' and len(command) == 2:
                try:
                    move_num = int(command[1])
                    if engine.goto_move(move_num):
                        self.view.display_success(f"Jumped to move {move_num}")
                    else:
                        self.view.display_error(f"Invalid move number (1-{total})")
                except ValueError:
                    self.view.display_error("Invalid move number")
            
            elif cmd == 'play':
                speed = 1.0
                if len(command) == 2:
                    try:
                        speed = float(command[1])
                    except ValueError:
                        pass
                engine.play_auto(self.view, delay=1.0/speed)
            
            elif cmd in ('exit', 'e'):
                break
            
            else:
                self.view.display_error("Invalid replay command")
