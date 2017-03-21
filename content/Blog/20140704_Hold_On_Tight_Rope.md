Title: Hold on Tight!
Date: 2014-07-04 09:29
Tags: physics
Image: 20140704_Hold_On_Tight_Rope/RopeFriction.png
Summary: There are quite a few places where one can go indoor rock climbing in NYC. To keep the climber safe, the climber wears a harness that is attached to to a rope. The rope is then wrapped around a pipe at least one time and then at least 160 degrees more depending on where your buddy is holding on to the other end. The amount of force needed to hold a climber up is surprisingly low because of how friction helps prevents the rope from slipping off the pipe.

There are quite a few places where one can go indoor rock climbing in NYC. To keep the climber safe, the climber wears a harness that is attached to to a rope. The rope is then wrapped around a pipe at least one time and then at least 160 degrees more depending on where your buddy is holding on to the other end. The amount of force needed to hold a climber up is surprisingly low because of how friction helps prevents the rope from slipping off the pipe.

Roughly, the rope that wraps around the pipe looks something like this:

![Rope friction]({filename}/images/20140704_Hold_On_Tight_Rope/RopeFriction.png)

The force that is used to hold the climber up is called a belaying force. To calculate the relationship between the force of the climber and the belaying force, we go back to undergraduate physics and draw a free body diagram of a small piece of the rope:

![Free body of rope]({filename}/images/20140704_Hold_On_Tight_Rope/ropefreebody.png)

where $T$ is tension at one end, $T+dT$ is the tension at the other end, $N$ is the normal force, and $f$ is the friction force that is resisting slipping. In equilibrium, we sum the forces in the vertical:

$$
\sum F_y = dN - T\sin\left(\dfrac{d\theta}{2}\right) - (T+dT)\sin\left(\dfrac{d\theta}{2}\right) = 0
$$

and horizontal directions:

$$
\sum F_x = T\cos\left(\dfrac{d\theta}{2}\right) - (T+dT)\cos\left(\dfrac{d\theta}{2}\right) + df = 0
$$

Since $d\theta$ is small, the trigonometric functions can be simplified as follows:

$$
\sin\left(\dfrac{d\theta}{2}\right) = \dfrac{d\theta}{2} \textrm{ and } \cos\left(\dfrac{d\theta}{2}\right) = 1
$$

With these simplifications the vertical equation becomes:

$$
\dfrac{dN}{d\theta} = T
$$

Recalling that $f=\mu N$ where $\mu$ is the static coefficient of friction, the horizontal equation becomes:

$$
\dfrac{dT}{d\theta} = \dfrac{df}{d\theta} = \mu\dfrac{dN}{d\theta}
$$

Putting the above two equations together, we get a simple differential equation:

$$
\dfrac{dT}{d\theta} = \mu T
$$

with the solution:

$$
T = T_0e^{\mu\theta}
$$

where $T_0$ is the tension of belaying force and $T$ is force from the climber. If you want to calculate the force required to hold a climber up, we just solve for $T_0$:

$$
T_0 = Te^{-\mu\theta}
$$

If the rope is wrapped around once and an addition 160 degrees, then theta is 160+360=520 degrees or 9.08 radians. Letting the coefficient of friction between a nylon rope and a steel pipe be 0.20 and weight of the climber be 120.0 lbs, then the force needed to hold the climber up is:

$$
T_0 = (120.0)e^{-(0.20)(9.08)} = 19.5\textrm{ lbs}
$$

In other words, we only need to provide 16.3% of the weight of the climber to hold him/her up. Hoping your buddy uses two hands, thats only 10 lbs of force per hand. Kind of crazy huh?

## Side Note

When ships dock, sailors use rope wrapped around a post to keep the ship from floating away. The rope is wrapped around the post several times like so:

![Posts]({filename}/images/20140704_Hold_On_Tight_Rope/posts.jpg)

In this picture, the rope wrapped around the post about five times. Assuming coefficient of friction is $0.20$, the knot tied to the dock only needs 0.2% of tugging force from to ship to keep it docked.
