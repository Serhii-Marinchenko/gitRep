const prompt = require('prompt-sync')({sigint: true});
const chars = ['^', 'O', '░', '*'];
const [hat, hole, fieldCharacter, pathCharacter] = chars;
const choises = ['u', 'd', 'l', 'r'];
const [l, d, u, r] = choises;
const names = ['Up', 'Down', 'Left', 'Right'];
let f
let f1


class Field {
  constructor(field) {
  	this._field = field
    this._rows = this._field.length
    this._columns = this._field[0].length
    this._playerPosition = undefined
    this._copy = []
    for (let i in field) {
      this._copy[i] = []
      for (let j in field[i]) {
        this._copy[i][j] = field[i][j]
      }
    }
  }
  get field() {
    return this._field
  }

  get rows() {
    return this._rows
  }

  get columns() {
    return this._columns
  }

  get playerPosition() {
    return this._playerPosition
  }

  static generateField(rows, columns, p) {
    const field = []
    let k = 0
    while (field.length < rows) {
      field[k] = []
      k++
    }
    for (let i in field) {
      while (field[i].length !== columns) {
        for (let j = 0; j < columns; j++) {
          let randInt = Math.random()
          field[i][j] = randInt > p ? fieldCharacter : hole
        }
      }
    }
    let count = 0
    for (let i in field) {
      for (let j in field[i]) {
        if (field[i][j] === hole) {
          count++
        }
      }
    }
    field[Math.floor(Math.random() * rows)][Math.floor(Math.random() * columns)] = hat
    return field
  }

  generatePosition() {
    return [Math.floor(Math.random() * this.rows), Math.floor(Math.random()*this.columns)]
  }

  setPlayerPosition() {
    const hatPos = this.getHatPosition(this.field)
    let playerPos = this.generatePosition()
    while (hatPos === playerPos || this.field[playerPos[0]][playerPos[1]] === 'O') {
      playerPos = this.generatePosition()
    }
    this._playerPosition = playerPos
    this._field[this.playerPosition[0]][this.playerPosition[1]] = pathCharacter
  }

  reset() {
    const copy2 = []
    for (let i in this._copy) {
      copy2[i] = []
      for (let j in this._copy[i]) {
        copy2[i][j] = this._copy[i][j]
      }
    }
    this._field = copy2
    this.setPlayerPosition()
  }

  changeChar(row, column, char) {
    if (this.gameOver()) {
      this.reset()
      return true
    }
    this._field[row][column] = char
  }

  print() {
    let s
  	for (let i = 0; i < this.rows; i++) {
      s = ''
      for (let j = 0; j < this.columns; j++){
        s += this.field[i][j]
      }
      console.log(s)
  	}
  }

  getHatPosition(arg) {
    let pos
    for (let i in arg) {
      for (let j in arg[i]) {
        if (arg[i][j] === hat) {
          pos = [i, j]
          break;
        }
      }
    }
    pos = pos ? pos : 'No hat in this field'
    return pos
  }

  gameOver() {
    const bad = this.playerPosition[1] >= this.columns || this.playerPosition[1] < 0 ||
                this.playerPosition[0] >= this.rows || this.playerPosition[0] < 0 ||
                this.field[this.playerPosition[0]][this.playerPosition[1]] === hole
    if (bad) {
      console.log('Game Over.')
      return true
    }
    const good = this.field[this.playerPosition[0]][this.playerPosition[1]] === hat
    if (good) {
      console.log('Victory!')
    }
    return good || bad
  }

  getInput() {
    for (let i in choises) {
      console.log(`Enter '${choises[i]}' for '${names[i]}'`)
    }
    let ans = prompt('Which way? ')
    for (let i = 0; i < choises.length; i++) {
      if (choises[i] === ans) {
        return ans
      }
    }
    console.log('\nInvalid move. Try again\n')
    return this.getInput()
    }

  play() {
    if (this.playerPosition === undefined) {
      this.setPlayerPosition()
    } else if (this.changeChar(this.playerPosition[0], this.playerPosition[1], pathCharacter)) {
      return
    }
    this.print()
    let move = this.getInput()
    switch (move) {
      case 'l':
        this.playerPosition[1]--
        break;
      case 'r':
        this._playerPosition[1]++
        break;
      case 'u':
        this._playerPosition[0]--
        break;
      case 'd':
        this._playerPosition[0]++
        break;
    }
    return this.play()
  }
}

f = Field.generateField(20, 40, 0.3)
f1 = new Field(f)
f1.play()