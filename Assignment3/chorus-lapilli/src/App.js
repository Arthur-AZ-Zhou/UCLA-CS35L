import { useState } from 'react';

var turnNum = 0;
let xArray = []
let oArray = []

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));

  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    } 
    
    if (turnNum >= 6) {
      if (xIsNext) {
        squares[xArray[0]] = null;
        xArray.shift();
      } else {
        squares[oArray[0]] = null;
        oArray.shift();
      }
    }

    const nextSquares = squares.slice();
    if (xIsNext) {
      if (checkValidMove(xIsNext, i)) {
        nextSquares[i] = 'X';
        xArray.push(i);
      } else {
        console.log("INVALID MOVE");
        return;
      }
    } else {
      if (checkValidMove(!xIsNext, i)) {
        nextSquares[i] = 'O';
        oArray.push(i);
      } else {
        console.log("INVALID MOVE");
        return;
      }
    }

    setSquares(nextSquares);
    setXIsNext(!xIsNext);
    turnNum++;
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function checkValidMove(isXNext, dest) { //returns true if valid false if otherwise
  if (turnNum < 6) {
    return true;
  }

  if (isXNext) {
    for (let i = 0; i < xArray.length; i++) {
      switch (xArray[i]) {
        case 0:
          if (dest === 1 || dest === 3 || dest === 4) {
            return true;
          }
          break;
        case 1: 
          if (dest === 0 || dest === 2 || dest === 3 || dest === 4 || dest === 5) {
            return true;
          }
          break;
        case 2: 
          if (dest === 1 || dest === 4 || dest === 5) {
            return true;
          }
          break;
        case 3:
          if (dest === 0 || dest === 1 || dest === 4 || dest === 6 || dest === 7) {
            return true;
          }
          break;
        case 4: 
          return true;
        case 5: 
          if (dest === 1 || dest === 2 || dest === 4 || dest === 7 || dest === 8) {
            return true;
          }
          break;
        case 6: 
          if (dest === 3 || dest === 4 || dest === 7) {
            return true;
          }
          break;
        case 7: 
          if (dest === 3 || dest === 4 || dest === 5 || dest === 6 || dest === 8) {
            return true;
          }
          break;
        case 8: 
          if (dest === 4 || dest === 5 || dest === 7) {
            return true;
          }
          break;
        default:
      }
    }
  } else {
    for (let i = 0; i < oArray.length; i++) {
      switch (oArray[i]) {
        case 0:
          if (dest === 1 || dest === 3 || dest === 4) {
            return true;
          }
          break;
        case 1: 
          if (dest === 0 || dest === 2 || dest === 3 || dest === 4 || dest === 5) {
            return true;
          }
          break;
        case 2: 
          if (dest === 1 || dest === 4 || dest === 5) {
            return true;
          }
          break;
        case 3:
          if (dest === 0 || dest === 1 || dest === 4 || dest === 6 || dest === 7) {
            return true;
          }
          break;
        case 4: 
          return true;
        case 5: 
          if (dest === 1 || dest === 2 || dest === 4 || dest === 7 || dest === 8) {
            return true;
          }
          break;
        case 6: 
          if (dest === 3 || dest === 4 || dest === 7) {
            return true;
          }
          break;
        case 7: 
          if (dest === 3 || dest === 4 || dest === 5 || dest === 6 || dest === 8) {
            return true;
          }
          break;
        case 8: 
          if (dest === 4 || dest === 5 || dest === 7) {
            return true;
          }
          break;
        default:
      }
    }
  }

  return false;
}

// import { useState } from "react";

// function Square( { value, onSquareClick }) {
//   return(
//     <button className="square" onClick={onSquareClick}>
//       {value}
//     </button>
//   ) 
// }

// function calculateWinner(squares) {
//   const lines = [
//     [0, 1, 2],
//     [3, 4, 5],
//     [6, 7, 8],
//     [0, 3, 6],
//     [1, 4, 7],
//     [2, 5, 8],
//     [0, 4, 8],
//     [2, 4, 6]
//   ];
//   for (let i = 0; i < lines.length; i++) {
//     const [a, b, c] = lines[i];
//     if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) { //3 in a row same as squares[a]
//       return squares[a];
//     }
//   }
//   return null;
// }

// function Board({ xIsNext, squares, onPlay }) {
//   // const [xIsNext, setXIsNext] = useState(true);
//   // const [squares, setSquares] = useState(Array(9).fill(null));

//   function handleClick(i) {
//     if (squares[i] || calculateWinner(squares)) {
//       return;
//     }

//     const nextSquares = squares.slice();
//     if (xIsNext) {
//       nextSquares[i] = "X";
//     } else {
//       nextSquares[i] = "O";
//     }
//     onPlay(nextSquares);
//   }

//   const winner = calculateWinner(squares);
//   let status;
//   if (winner) {
//     status = "Winner: " + winner;
//   } else {
//     status = "Next player: " + (xIsNext ? "X" : "O");
//   }

//   return (
//     <>
//       <div className="board-row">
//         <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
//         <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
//         <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
//       </div>
//       <div className="board-row">
//         <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
//         <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
//         <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
//       </div>
//       <div className="board-row">
//         <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
//         <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
//         <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
//       </div>
//     </>
//   );
// }

// export default function Game() {
//   const [history, setHistory] = useState([Array(9).fill(null)]);
//   const [currentMove, setCurrentMove] = useState(0);
//   const xIsNext = (currentMove % 2 === 0);
//   const currentSquares = history[currentMove];

//   function handlePlay(nextSquares) {
//     const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
//     setHistory(nextHistory);
//     setCurrentMove(nextHistory.length - 1);
//   }

//   function jumpTo(nextMove) {
//     setCurrentMove(nextMove);
//   }

//   const moves = history.map((squares, move) => {
//     let description;
//     if (move > 0) {
//       description = 'Go to move #' + move;
//     } else {
//       description = 'Go to game start';
//     }
//     return (
//       <li key={move}>
//         <button onClick={() => jumpTo(move)}>{description}</button>
//       </li>
//     );
//   });

//   return (
//     <div className="game">
//       <div className="game-board">
//         <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
//       </div>
//       <div className="game-info">
//         <ol>{moves}</ol>
//       </div>
//     </div>
//   )
// }