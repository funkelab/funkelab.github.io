---
layout: page
title: QuAC
description: Quantitative Attribution with Counterfactuals
img: assets/img/teasers/quac.png
importance: 1
category: explainable AI
related_publications: true
---

<img src="/assets/img/teasers/quac.png" class="img-fluid" style="width: 100%;" alt="overview of QuAC" />
{% cite adjavon_2024_quantitative %}

We address the problem of explaining the decision process of deep neural
network classifiers on images, which is of particular importance in biomedical
datasets where class-relevant differences are not always obvious to a human
observer.

Our proposed solution, termed quantitative attribution with counterfactuals
(QuAC), generates visual explanations that highlight class-relevant differences
by attributing the classifier decision to changes of visual features in small
parts of an image.

To that end, we train a separate network to generate counterfactual images
(i.e., to translate images between different classes). We then find the most
important differences using novel discriminative attribution methods.

Crucially, QuAC allows scoring of the attribution and thus provides a measure
to quantify and compare the fidelity of a visual explanation.

We demonstrate the suitability and limitations of QuAC on two datasets: (1) a
synthetic dataset with known class differences, representing different levels
of protein aggregation in cells and (2) an electron microscopy dataset of
*Drosophila* synapses with different neurotransmitters, where QuAC reveals so
far unknown visual differences. 

We further discuss under which conditions datasets should be collected to allow
methods like QuAC to provide insight into class-relevant features, and how
those insights can be used to derive novel biological hypotheses.
