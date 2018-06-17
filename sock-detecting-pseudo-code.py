

Available colours
Red (colour range)
Blue (colour range)
Green (colour range)
Yellow (colour range)
Pink (colour range)
Background colour (colour range)


turn on camera lights

When button pressed, "Want to start matching socks?"
If button pressed, start
while true
	Move conveyor stepper.
	analyse camera image
	If not detecting background range, look at colour
	- if colour is in range of one of the colours, move that bin in place.
	- else move the unmatched bin in place.
	- say what colour was detected.
		- if colour already has two socks, say so and put in unmatched bin.

	If stop pressed
	- say which colours were matched.