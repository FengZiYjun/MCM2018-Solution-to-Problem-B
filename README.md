# Solution to Problem B of MCM 2018

Problem B of MCM 2018 can be found here. ![](https://www.comap.com/undergraduate/contests/)

We implemented the **Bilinguals Model** that was proposed in the paper *Agent Based Models of Language Competition: Macroscopic descriptions and Order-Disorder transitions*.

The Abrams-Strogatz model explored the evolution of two languages where the speakers are the nodes in a massive social network of interaction. The probability that one language speaker changes its language to the other depends on the *prestige* of the language, the density of neighboring speakers of this individual, and the volatility parameter.
$$P(XY) = (1-S) \sigma_y^alpha$$

The **Bilinguals Model** is an extension of the Abrams-Strogatz model. It introduced the bilinguals - individuals who speak both the first and second languages. A monolingual will become a bilingual by learning a second language with a probability related to the language prestige, the language density among neighbors, and the volatility. Also a bilingual will forget one language and become a monolingual with another probability. 

Given the bilingual model and the social network architecture, we can know how the number of speakers of each language changes.

In our implementation, multiple languages are considered in pairs to determine the influence towards each other.
