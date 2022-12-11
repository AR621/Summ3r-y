ex_prompt_1 = """
Many people cherished under the rule of muhammad II while many were 
impoverished under his son's reign who ruled more like a tyrant than a proper ruler"""
qchnn_good = """
Results of QCCNN’s analysis show that the network was able to reach higher accuracy
than the classical analogue as seen on figure 5.1. While this certainly seems lucrative we
can still achieve higher accuracy with classical ML methods by simply adding more layers
to the network or using different approaches, such as transfer learning

While a quantum advantage on classical data still remains to be proven, we can think
that perhaps quantum computers within NN architectures would allow us to expose some
linear features which are more easily distinguishable when using QC. This very point calls
for further investigation but if proven would mean that using such hybrid architectures
would allow us to get higher accuracy of models which wouldnt be possible without any
classical ML algorithms and thus would potentially offset the costs of quantum hardware.

The explored architectures show a potential when it comes to achieving faster training
results. QTL in particular has shown that it converges to the near minima levels faster
when compared to their classical counterpart. This is visible on all accuracy results of
QML subsection although most prominent on figure 5.5

This may be due to - again - quantum part of the network being more inclined to distinguish nonlinear features within the dataset which means that the network overall has an
easier time distinguishing the two classes, which in turn results in this phenomena.

Development of quantum algorithms may improve our knowledge about quantum physics
since it allows us to interact with the quantum data directly without first quantitizing it.
56 6. Conclusions
We do not know whether large scale quantum computers which can work independently
from classical computers (apart from operating the quantum hardware) will exist but
if they do, the developed algorithms will be ready for implementation and use. The
developed quantum algorithms can also potentially bring insights back to the classical
world and improve existing classical algorithms which are basis for developing the quantum
 algorithms"""
qchnn_bad = """
The experiments performed with QC simulators showed also some potential weaknesses
 of hybrid architectures.
A first notable weakness would be that these networks in general seem to vary more in the
results that can be achieved with them from epoch to epoch basis when compared with
classical analogue as presented in subchapter 4.3.1 - exploration of QCCNN’s which was
specifically visible with 1 layer and 3 layer quanvolution layers as seen on figure 5.1. While
the general accuracy achieved was higher, it also seemed to be more unstable between
consecutive epochs, on epoch 11 and 28 specifically we can see it went down considerably
- to the similar levels of accuracy achieved by the rest of architectures.
It is also important to point out that current quantum devices implement a lot of noise
and thus we may conclude that this instability would be even more visible on real quantum
devices when compared to simulations results showcased in this work.
The similar can be drawn for QTL methods as seen with their sensitivity to changing
hyperparameters. Exploration of this architecture has shown that hyperparameter tuning
is an even more important aspect in QTL that in classical TL and we may conclude that
this importance would be even more amplified if we were to use a real quantum computer
for this architecture. While these networks may potentially bring benefits in their current
state it would seem like tuning them will also be a harder challenge.
When it comes to QGAN’s, they would also be most likely affected by the noise implemented 
by NISQ era QC, however the authors point out that they could be more resistant
to it[29].

An obvious point is that implementation of such hybrid architecture will first of all require
a quantum computer, even if such architecture could be realised by using cloud architectures 
via connecting to publicly available computer or a one that we bought calculation
time on - this still means the algorithms need to be realized in some part differently to
allow for such model to learn.
This may be in part mitigated by architectures such as presented QCCNN which allows
to firs use QC to process and save the images and then they can be processed as a normal
NN, however The very early advancement - and price - of quantum architecture means
that for now it still remains a challenge and means that they are potentially not viable
to implement if no quantum advantage will be harnessed from them"""
qchnn_end = """
Quantum computing is an emerging field that could bring us potential advantages in many
modern day problems[42][38][12][10] however much remains to be done in this field for
Quantum Computing to be a viable approach in solving them. We do not know whether
QC will be adapted to a wide scale in the future or will remain only as a small subfield
of Information Theory developed only for research purposes or very specific problems, in
which it can be easily harnessed for an advantage such as cryptography [10] or factorization
of numbers [42]. The thing that remains sure however is that for now it is actively being
researched and if not bringing advantages by itself, it can bring us insights about quantum
world around us and the classical algorithms that we try to implement into quantum world,
which might bring improvements to them as well."""
