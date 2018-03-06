# Solution to Problem B of MCM 2018

Problem B of MCM 2018 can be found here. ![](https://www.comap.com/undergraduate/contests/)

We implemented the **Bilinguals Model** that was proposed in the paper *Agent Based Models of Language Competition: Macroscopic descriptions and Order-Disorder transitions*.

The Abrams-Strogatz model explored the evolution of two languages where the speakers are the nodes in a massive social network of interaction. The probability that one language speaker changes its language to the other depends on the *prestige* of the language <img src="https://latex.codecogs.com/svg.latex?\Large&space;S" title=""/>, the density of neighboring speakers of language X around this individual  <img src="https://latex.codecogs.com/svg.latex?\Large&space;\sigma_X" title=""/>, and the volatility parameter <img src="https://latex.codecogs.com/svg.latex?\Large&space;\alpha" title=""/>.

<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(X{\rightarrow}Y)=(1-S)\sigma_{Y}^{\alpha}" title="\Large P(XY) = (1-S) \sigma_y^alpha" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(Y{\rightarrow}X)=S\sigma_{X}^{\alpha}" title="\LargeP(Y{\rightarrow}X)=S\sigma_{X}^{\alpha}" />


The **Bilinguals Model** is an extension of the Abrams-Strogatz model. It introduced the bilinguals - individuals who speak both the first and second languages. A monolingual will become a bilingual by learning a second language with a probability related to the language prestige, the language density among neighbors, and the volatility. Also a bilingual will forget one language and become a monolingual with another probability. 


<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(X{\rightarrow}XY)=(1-S)\sigma_{Y}^{\alpha}" title="\Large P(XY) = (1-S) \sigma_y^alpha" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(Y{\rightarrow}YX)=S\sigma_{X}^{\alpha}" title="\LargeP(Y{\rightarrow}X)=S\sigma_{X}^{\alpha}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(XY{\rightarrow}X)=(1-S)(1-\sigma_{X})^{\alpha}" title="\LargeP(Y{\rightarrow}X)=S\sigma_{X}^{\alpha}" />
<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(XY{\rightarrow}Y)=S(1-\sigma_{Y})^{\alpha}" title="\LargeP(Y{\rightarrow}X)=S\sigma_{X}^{\alpha}" />



Given the bilingual model and the social network architecture, we can know how the number of speakers of each language changes.

In our implementation, multiple languages are considered in pairs to determine the influence towards each other.
