import random

class QuantumParticle:
    def __init__(self, x=0, y=0, p=0):
        self._position = x      # renamed attribute
        self._momentum = y      # renamed attribute
        self._spin = p          # renamed attribute
        self.entangled_particle = None

    def position(self):
        """Measure position — triggers disturbance."""
        self._disturb()
        return self._position

    def momentum(self):
        """Measure momentum — triggers disturbance."""
        self._disturb()
        return self._momentum

    def spin(self):
        """Measure spin — triggers disturbance, and syncs entangled partner."""
        self._disturb()
        if self.entangled_particle:
            # Opposite spin on the entangled particle (no disturbance triggered there)
            self.entangled_particle._spin = -self._spin
        return self._spin

    def _disturb(self):
        """Internal: called every time a measurement is made."""
        self._position = random.randint(1, 10000)
        self._momentum = random.uniform(0, 1)
        self._spin = random.choice([-0.5, 0.5])
        print('Quantum Interferences!!')

    def entangle(self, other_particle):
        if isinstance(other_particle, QuantumParticle):
            self.entangled_particle = other_particle
            other_particle.entangled_particle = self
            print('Spooky Action at a Distance !!')
        else:
            print("Can only entangle with another QuantumParticle.")

    def __repr__(self):
        return (f"QuantumParticle(position={self._position}, "
                f"momentum={self._momentum}, spin={self._spin})")


# --- Test ---
p1 = QuantumParticle(x=1, p=5.0)
p2 = QuantumParticle(x=2, p=5.0)
p1.entangle(p2)

print(p1.position())   # triggers disturbance
print(p1.spin())       # triggers disturbance + sets p2's spin to opposite
print(f"p2 spin: {p2._spin}")  # should be opposite of p1's spin