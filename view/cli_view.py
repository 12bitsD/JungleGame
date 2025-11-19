"""
CLI View for Jungle Game.
Handles console display and user input.
"""

from model import Board, GameState, Player, GameStatus, MoveValidator


class CLIView:
    """Console-based view for the game."""
    
    def __init__(self):
        self.board = None
    
    def display_board(self, board: Board, highlight_positions: list = None):
        """Display the game board in console."""
        if highlight_positions is None:
            highlight_positions = []
        
        print("\n" + "=" * 50)
        print("  " + "  ".join([Board.col_to_letter(c) for c in range(Board.COLS)]))
        print("  " + "-" * (Board.COLS * 3))
        
        # Display from top to bottom (BLUE side at top)
        for row in range(Board.ROWS - 1, -1, -1):
            row_display = f"{Board.row_to_number(row)} "
            for col in range(Board.COLS):
                piece = board.get_piece(row, col)
                terrain = board.get_terrain(row, col)
                
                if piece:
                    symbol = piece.get_symbol()
                else:
                    # Show terrain indicators
                    if terrain.value == "WATER":
                        symbol = "≈"
                    elif terrain.value == "TRAP":
                        symbol = "△"
                    elif terrain.value == "DEN":
                        symbol = "■"
                    else:
                        symbol = "·"
                
                # Highlight if position is in highlight list
                if (row, col) in highlight_positions:
                    symbol = f"[{symbol}]"
                else:
                    symbol = f" {symbol} "
                
                row_display += symbol
            
            print(row_display)
        
        print("  " + "-" * (Board.COLS * 3))
        print("=" * 50)
        
        # Legend
        print("\nLegend:")
        print("  RED pieces: lowercase (r=Rat, c=Cat, d=Dog, w=Wolf, l=Leopard, t=Tiger, n=Lion, e=Elephant)")
        print("  BLUE pieces: UPPERCASE (R=Rat, C=Cat, D=Dog, W=Wolf, L=Leopard, T=Tiger, N=Lion, E=Elephant)")
        print("  Terrain: ≈=Water, △=Trap, ■=Den, ·=Normal")
    
    def display_game_status(self, game_state: GameState):
        """Display current game status."""
        print(f"\nCurrent Player: {game_state.current_player.value}")
        print(f"Move Number: {len(game_state.move_history) + 1}")
        print(f"Moves without capture: {game_state.move_count_no_capture}/{GameState.MAX_MOVES_WITHOUT_CAPTURE}")
        
        # Show captured pieces
        for player in [Player.RED, Player.BLUE]:
            captured = game_state.captured_pieces[player]
            if captured:
                opponent = Player.BLUE if player == Player.RED else Player.RED
                pieces_str = ", ".join([p.get_name() for p in captured])
                print(f"{opponent.value} captured: {pieces_str}")
    
    def display_move_history(self, game_state: GameState, last_n: int = 10):
        """Display recent moves."""
        if not game_state.move_history:
            print("\nNo moves yet.")
            return
        
        print(f"\n--- Last {last_n} Moves ---")
        recent_moves = game_state.move_history[-last_n:]
        for move in recent_moves:
            print(f"  {move.to_notation(game_state.board)}")
    
    def display_legal_moves(self, board: Board, piece, legal_moves: list):
        """Display legal moves for a piece."""
        if not legal_moves:
            print(f"\nNo legal moves for {piece.get_name()} at {board.position_to_notation(piece.row, piece.col)}")
            return
        
        print(f"\nLegal moves for {piece.get_name()} at {board.position_to_notation(piece.row, piece.col)}:")
        for row, col in legal_moves:
            notation = board.position_to_notation(row, col)
            target_piece = board.get_piece(row, col)
            if target_piece:
                print(f"  {notation} (capture {target_piece.get_name()})")
            else:
                print(f"  {notation}")
    
    def get_user_input(self, prompt: str) -> str:
        """Get input from user."""
        return input(prompt).strip()
    
    def display_message(self, message: str):
        """Display a message to user."""
        print(f"\n{message}")
    
    def display_error(self, error: str):
        """Display an error message."""
        print(f"\n❌ Error: {error}")
    
    def display_success(self, message: str):
        """Display a success message."""
        print(f"\n✓ {message}")
    
    def display_menu(self):
        """Display main menu options."""
        print("\n" + "=" * 50)
        print("JUNGLE GAME (斗兽棋)")
        print("=" * 50)
        print("\nCommands:")
        print("  move <from> <to>  - Make a move (e.g., 'move E3 E4')")
        print("  show <pos>        - Show legal moves for piece (e.g., 'show E3')")
        print("  undo              - Undo last move")
        print("  redo              - Redo undone move")
        print("  history           - Show move history")
        print("  save <filename>   - Save game")
        print("  load <filename>   - Load game")
        print("  new               - Start new game")
        print("  replay            - Enter replay mode")
        print("  quit              - Exit game")
        print("=" * 50)
    
    def display_game_over(self, game_status: str, game_state: GameState):
        """Display game over message."""
        print("\n" + "=" * 50)
        print("GAME OVER")
        print("=" * 50)
        
        if game_status == GameStatus.RED_WIN:
            print("\n🎉 RED WINS!")
        elif game_status == GameStatus.BLUE_WIN:
            print("\n🎉 BLUE WINS!")
        elif game_status == GameStatus.DRAW:
            print("\n🤝 GAME DRAWN")
        
        print(f"\nTotal moves: {len(game_state.move_history)}")
        print("=" * 50)
    
    def confirm_action(self, prompt: str) -> bool:
        """Ask for yes/no confirmation."""
        response = input(f"\n{prompt} (y/n): ").strip().lower()
        return response in ('y', 'yes')
    
    def display_replay_controls(self):
        """Display replay mode controls."""
        print("\n" + "-" * 50)
        print("REPLAY MODE")
        print("-" * 50)
        print("Commands:")
        print("  next / n      - Step forward")
        print("  prev / p      - Step backward")
        print("  goto <num>    - Jump to move number")
        print("  play          - Auto-play remaining moves")
        print("  exit / e      - Exit replay mode")
        print("-" * 50)
    
    def clear_screen(self):
        """Clear the console screen (optional)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
