# Tutorial Script

## First interaction

At the beginning, there is nothing. All buttons are interactible, but they don't do anything.
If the player clicks at the grid, the first cell is "placed" and next to it a big red **!** is created.
The message "Wow! You have created live in this desolate place! Do you think it survives until the next generation?"
is displayed and "next generation" is a reference to the "next generation" Button.

## Second interaction

Here it gets interesting, lets look at our options.

### "One dying cell"

The player has placed exactly one cell and starts the "next generation".

Whats supposed to happen:

- [Rule unlocked: Underpopulation (not directly part of tutorial)]
- Message: "It seems a single cell can't survive alone."

### "Two dying cells"

The player has placed exactly two cell and starts the "next generation".

Whats supposed to happen:

- [(Rule gets triggered here, if not done so previously)]
- Message: "Maybe it needs more cells in its neighbourhood!?"

### "Three dying cells"

The player has placed exactly three cell and starts the "next generation" wich causes all cells to die.

Whats supposed to happen:

- [(Rule gets triggered here, if not done so previously)]
- Message: "What do you think happens when you put them all as close together as possible?"

### "Three cells with a survivor"

The player places exactly three cells and starts the "next generation" which causes just one cell to survive.

Whats supposed to happen:

- [Rule unlocked: Survival]
- Message: "Amazing! It seems one of them survived! How about we just add more cells?!"

### "Blinker"

The player places exactly three cells and starts the "next generation" which causes just one cell to survive, two to die and two to be born.

Whats supposed to happen:

- [Achievement unlocked: Blinker]
- [Rule unlocked: Reproduction]
- Message: "Wow! It seems to be stable! Congratulation! You created a stable world! This one will survive on its own after starting the evolution!"

## Afterwords

After these inital interactions the player should have enough information to proceed to play around with the world.
Hopefully...
