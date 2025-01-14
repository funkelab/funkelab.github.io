---
layout: page
title: blinx
description: Counting of Fluorescent Emitters in Diffraction Limited Spots
img: assets/img/teasers/blinx.png
importance: 4
category: microscopy
related_publications: true
---

<img src="/assets/img/teasers/blinx.png" class="img-fluid" style="width: 100%;" alt="overview of blinx" />
{% cite hillsley_2024_bayesian %}

We address the problem of inferring the number of independently blinking
fluorescent light emitters, when only their combined intensity contributions
can be observed at each timepoint.

This problem occurs regularly in light microscopy of that are smaller than the
diffraction limit, where one wishes to count the number of fluorescently
labelled.

Our proposed solution directly models the photo-physics of the system, as well
as the blinking kinetics of the fluorescent emitters as a fully differentiable.

Given a trace of intensity over time, our model jointly estimates the
parameters of the intensity distribution per emitter, their blinking rates, as
well as a posterior distribution of the total number of fluorescent emitters.

We show that our model is consistently more accurate and increases the range of
countable subunits by a factor of two compared to current state-of-the-art
methods, which count based on autocorrelation and blinking frequency.

Furthermore, we demonstrate that our model can be used to investigate the
effect of blinking kinetics on counting ability, and therefore can inform
experimental conditions that will maximize counting accuracy.
