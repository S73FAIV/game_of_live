# Conway´s Game of Live

## Architecture:

For the Main Components of the Game we use the **Model-Controller-View**-Pattern (MCV). Where the game_state captures the state of the game and simulates its automatic updates, the controller is the only one, that changes the game_state from externally and all other components, that rely on the game_state get their updates via a event_bus.

The game_state is closely connected to a PatternAnalyzer, that will do all the logic for us to see, if a new achievement was triggered and emits events accrodingly to the bus.
From there the Achievement- and Tutorial-Manager can interpret those events.

## Attributions:

### Pictures/Icons

<a href="https://www.flaticon.com/free-icons/mute" title="mute icons">Mute icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/speaker" title="speaker icons">Speaker icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/tools-and-utensils" title="Tools and utensils icons">Tools and utensils icons created by Google - Flaticon</a>

### Music

<a href="https://pixabay.com/music/pop-lofi-loop-hopeful-city-321581/" title="Pixabay Lofi Loop Hopeful City">Pixabay Lofi Loop Hopeful City</a>


### Not yet integrated:

<a href="https://www.flaticon.com/free-icons/verification" title="verification icons">Verification icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/check-circle" title="check circle icons">Check circle icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/fast-forward" title="fast forward icons">Fast forward icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/next" title="next icons">Next icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/pause" title="pause icons">Pause icons created by Google - Flaticon</a>
<a href="https://www.flaticon.com/free-icons/achievement" title="achievement icons">Achievement icons created by VectorPortal - Flaticon</a>
