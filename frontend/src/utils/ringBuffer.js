export class RingBuffer {

  elements = []
  tail = 0
  head = 0
  capacity

  constructor(capacity) {
    this.capacity = capacity
    for (let i = 0; i < capacity; i++)
      this.elements.push(null)
  }

  enqueue = (element) => {
    if (this.tail - (this.head + 1) % this.capacity !== 0) {
      this.elements[this.head++] = element
      this.head = this.head === this.capacity ? 0 : this.head
      return true
    }

    return false
  }

  dequeue = () => {
    if (this.tail !== this.head) {
      const element = this.elements[this.tail++]
      this.tail = this.tail === this.capacity ? 0 : this.tail
      return element
    }

    return null
  }

  peek = () => {
    return this.elements[this.tail]
  }
}