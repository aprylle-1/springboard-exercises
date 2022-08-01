/** Connect Four
 *
 * Player 1 and 2 alternate turns. On each turn, a piece is dropped down a
 * column until a player gets four-in-a-row (horiz, vert, or diag) or until
 * board fills (tie)
 */

const WIDTH = 7;
const HEIGHT = 6;

let currPlayer = 1; // active player: 1 or 2
let board = []; // array of rows, each row is array of cells  (board[y][x])

/** makeBoard: create in-JS board structure:
 *   board = array of rows, each row is array of cells  (board[y][x])
 */

class Game {
  constructor(width, height, player1, player2){
    this.width = width
    this.height = height
    this.board = []
    this.player1 = player1
    this.player2 = player2
    this.currPlayer = 1
  }
  makeBoard(){
    for (let y = 0; y < this.height; y++) {
      this.board.push(Array.from({ length: this.width }));
    }
  }
  makeHtmlBoard(){
    const board = document.getElementById('board');
    const top = document.createElement('tr');
    top.setAttribute('id', 'column-top');
    const handleClick = this.handleClick.bind(this);
    top.addEventListener('click', handleClick);
  
    for (let x = 0; x < this.width; x++) {
      const headCell = document.createElement('td');
      headCell.setAttribute('id', x);
      top.append(headCell);
    }
  
    board.append(top);
  
    // make main part of board
    for (let y = 0; y < this.height; y++) {
      const row = document.createElement('tr');
  
      for (let x = 0; x < this.width; x++) {
        const cell = document.createElement('td');
        cell.setAttribute('id', `${y}-${x}`);
        row.append(cell);
      }
  
      board.append(row);
    }
  }
  findSpotForCol(x){
  for (let y = this.height - 1; y >= 0; y--) {
    if (!this.board[y][x]) {
      return y;
    }
  }
  return null;
  }
  placeInTable(y, x) {
  const piece = document.createElement('div');
  piece.classList.add('piece');
  if(this.currPlayer === 1){
    piece.style.backgroundColor = this.player1.color;
  }
  else{
    piece.style.backgroundColor = this.player2.color;
  }
  piece.style.top = -50 * (y + 2);
  const spot = document.getElementById(`${y}-${x}`);
  spot.append(piece);
  }
  checkForWin() {
  function _win(cells) {
    // Check four cells to see if they're all color of current player
    //  - cells: list of four (y, x) cells
    //  - returns true if all are legal coordinates & all match currPlayer
    return cells.every(
      ([y, x]) =>
        y >= 0 &&
        y < this.height &&
        x >= 0 &&
        x < this.width &&
        this.board[y][x] === this.currPlayer
    );
  }
  const __win = _win.bind(this)
  for (let y = 0; y < this.height; y++) {
    for (let x = 0; x < this.width; x++) {
      // get "check list" of 4 cells (starting here) for each of the different
      // ways to win
      const horiz = [[y, x], [y, x + 1], [y, x + 2], [y, x + 3]];
      const vert = [[y, x], [y + 1, x], [y + 2, x], [y + 3, x]];
      const diagDR = [[y, x], [y + 1, x + 1], [y + 2, x + 2], [y + 3, x + 3]];
      const diagDL = [[y, x], [y + 1, x - 1], [y + 2, x - 2], [y + 3, x - 3]];

      // find winner (only checking each win-possibility as needed)
      if (__win(horiz) || __win(vert) || __win(diagDR) || __win(diagDL)) {
        return true;
      }
    }
  }
  } 
  endGame(msg) {
    window.setTimeout(alert(msg), 1000);
  }
  handleClick(evt){
    const x = evt.target.id;
    const y = this.findSpotForCol(x);
    if (y === null){
      return
    }
    this.board[y][x] = this.currPlayer
    this.placeInTable(y,x)
    if (this.checkForWin()) {
      setTimeout(() => {
        this.endGame(`Player ${this.currPlayer} won!`);
      }, 500)
      const board = document.getElementById('board')
      board.style.pointerEvents = "none";
    }
    else if (this.board.every(row => row.every(cell => cell))) {
      setTimeout(()=>{
        this.endGame('Tie!')
      }, 500)
    }
    else{
      this.currPlayer = this.currPlayer === 1 ? 2 : 1;
    }
  }
}

class Player{
  constructor(color){
    this.color = color;
  }
}
const newGameBtn = document.getElementById('new-game')
newGameBtn.addEventListener('click', ()=>{
  const board = document.getElementById('board')
  board.innerHTML = '';
  board.style.pointerEvents = null;
  const player1Color = document.getElementById('player1')
  const player2Color = document.getElementById('player2')
  if(player1Color.value.toLowerCase() === player2Color.value.toLowerCase()){
    alert('Players have the same color')
    setTimeout(() =>{
        player1Color.value = ""
        player2Color.value = ""
    }, 500)
  }
  else{
    const player1 = new Player(player1Color.value);
    const player2 = new Player(player2Color.value);
    const game = new Game(WIDTH, HEIGHT, player1, player2)
    game.makeBoard();
    game.makeHtmlBoard();
  }
})
