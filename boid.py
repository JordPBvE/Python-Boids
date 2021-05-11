class Boid:
    def __init__(self): # window as input aswell??
        self.pos = (random.random , )
        self.velocity = random.random(0.9, 1)
        self.time = random.random(0.0, 10000) # perlin noise for angle noise?


    def draw(self):
        # draw with pygame
        print("") # error otherwise, can be deleted when other code is written

    def changeVelocity(self, boidArray):
        # self.angle += perlin(self.time)
        v1 = rule1(self, boidArray)
        v2 = rule2(self, boidArray)
        v3 = rule3(self, boidArray)

        self.velocity = self.velocity + v1 + v2 + v3

    def rule1():
        print("") 
    def rule2():
        print("")
    def rule3():
        print("")


### time input for noise function
  # def timeChange(self):
  #   self.time += 1

  # def move(self):



