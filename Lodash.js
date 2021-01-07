let _ = {
  clamp(number, lower, upper) {
    const lowerClampedValue = Math.max(number, lower)
    const clampedValue = Math.min(lowerClampedValue, upper)
    return clampedValue
  },
  inRange(number, start, end) {
    if (end === undefined) {
      end = start
      start = 0}
    if (start > end) {
      const blank = end
      end = start
      start = blank
    }
    const isInRange = start <= number &&
    number < end
    return isInRange
  },
  words (s) {
    return s.split(' ')
  },
  pad (string, length) {
    function addl (i, s) {
      let x = ' ' + s
      if (i === 0) {
        return x 
      } else {
        return addr(i-1, x)
      }
    }
    function addr (i, s) {
      let x = s + ' '
      if (i === 0) {
        return x
      } else {
        return addl(i-1, x)
      }
    }
    if (string.length >= length) {
      return string
    } else {
      let l = length - string.length
      return addr(l-1, string)
    }
  },
  has(object, key) {
    return object[key] !== undefined
  },
  invert(object) {
    let obj = {}
    for (let i in object) {
        obj[object[i]] = i
       //console.log(object[i][0])
      }
      return obj
    },
    findKey(object, f) {
      let pairs = Object.entries(object)
      let i = 0
      while (i < pairs.length) {
        let aux = f(pairs[i][1])
        if (aux) {
          return pairs[i][0]
          break
        } else {
          i++
        }
      }
    },
    drop(array, n) {
      return (n?
      array.slice(n):
      array.slice(1))
    },
    dropWhile (array, predicate) {
          function aux (index, array) {
          let tl = array.slice(1)
          let hd = array[0]
           if (predicate(hd, index, array)){
           return aux(index+1, tl)
      } else {
        return array
          } 
      }
    return aux(0, array)
      },

    chunk(array, size) {
      size = (size === undefined ? 1: size)
      let acc = [[array[0]]]
      let j = 0
      for (let i = 1; i < array.length; i++) {
        if ((i % (size)) === 0) {
          j++
          acc[j] = [array[i]]
        } else {
            acc[j].push(array[i])
          }
        }
        return acc
    }
}
