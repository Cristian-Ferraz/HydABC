# Presentation
<div style='text-align: justify'> Because of the intensive use of fossil fuels as the main energy source in modern society, mankind faces serious challenges against the consequences of the high amounts of greenhouse gas annually emitted. This way, much research has been conducted on the development of new sources of renewable energy, such as the utilization of biomass for H₂ generation through dark fermentation. Amidst the potential microorganisms capable of bioenergy production via fermentation, <i>Escherichia coli</i> stands out due to its position as a model organism, being highly described and utilized in different types of experiments. Furthermore, as a facultative anaerobic organism, <i>E. coli</i> metabolism shows great flexibility for metabolic engineering studies since it has the machinery for the metabolization of a large range of common compounds. </div><br>

<div style='text-align: justify'>However, regarding H₂ generation in <i>E. coli</i>, the native pathway leads to only 2 moles of H₂ per mole of glucose consumed, by the activity of pyruvate:formate lyase (PFL) (Reaction 1) and the formate:hydrogen lyase complex (Reaction 2):</div><br>

<p align="center">
pyruvate + CoA → formate + acetyl-CoA (Reaction 1)
</p>

<p align="center">
formate → H₂ + CO₂ (Reaction 2)
</p>

<div style='text-align: justify'>On the other hand, strict anaerobic species demonstrate high potential to synthesize biohydrogen through dark fermentation by the activity of specific hydrogenases, such as the hydrogenase ABC (HydABC) complex from the bacterium <i>Thermotoga maritima</i>, responsible for the transfer of e⁻ from NADH and reduced ferredoxin (Fd<sub>red</sub>) to protons H⁺ via an electron bifurcating mechanism (Schut and Adams, 2009) (Reaction 3).</div><br>

<p align="center">
Fd<sub>red</sub><sup>2−</sup> + NADH + 3H<sup>+</sup> → Fd<sub>ox</sub> + 2H₂ + NAD<sup>+</sup> (Reaction 3)
</p>

<p align="center">
ΔG° = +21 kJ
</p>

<div style= 'text-align: justify'> Therefore, as <b>suggested</b> by (Reaction 3), the HydABC complex could mediate the production of good amounts of H₂ if supported by enough concentration of NADH and Fd<sub>red</sub>, with emphasis on NADH, a very common cofactor present in a wide range of organisms. From the perspective of the pathways that lead to NADH generation, one can observe the tricarboxylic acid (TCA) cycle as a potential provider of the cofactor to the HydABC complex if operating on the reductive branch, since 3 moles of NADH are produced per turn of the cycle (Cao et al., 2022). Nevertheless, HydABC complex activity shows complete inhibition if in contact with even traces of O<sub>2</sub>, demanding the activity of the reductive branch under anaerobic conditions.</div><br> 

<div style='text-align: justify'> Accordingly, here, we provide a meticulous analysis of the capacity of biohydrogen production by the HydABC complex from <i>T. maritima</i> when heterologously expressed in the bacterium <i>E. coli</i>. To evaluate the maximum yield of H₂ production through the complex, the iCH360 (Corrao et al., 2025) genome-scale model will be used, serving as a basis to metabolic engineering simulations, such as flux balance analysis (FBA) and growth couple algorithms (Orth et al., 2010; Schneider et al., 2022). Also, in the last steps of the analysis, the thermodynamics of H₂ synthesis by HydABC will be elucidated, taking into account the native pathways present in <i>E. coli</i> before the expression (Beber et al., 2022). Below are indicated the main objectives of the project: </div><br>

<b>Main objective</b>: Evaluate the capacity of H₂ production by the HydABC complex from <i>T. maritima</i> when heterologously expressed in bacterium <i>E. coli</i> and supported by NADH production of the TCA cycle.

Secondary objectives: 
<ol>
    <li>Determine the main enzymes responsible for NADH generation through the TCA cycle under anaerobic conditions.</li>
    <li>Evaluate H₂ production by the HydABC complex after maximization of NADH through the TCA cycle.</li>
    <li>Establish the principal gene knockouts responsible for the maximization of H₂ production by the HydABC complex.</li>
    <li>Evaluate maximum H₂ production by the HydABC complex before its operation in reverse direction.</li>
</ol>

<div style='text-align: justify'>All codes generated can be found in files:</div>
<ul>
    <li><b>Part_1:</b> Initial Simulations on iCH360 </li>
    <li><b>Part_2:</b> Data Preparation</li>
    <li><b>Part_3:</b> Generation of Data for Use in the Machine Learning Model</li>
    <li><b>Part_4:</b> Data Configuration</li>
    <li><b>Part_5_1:</b> Class Creation for Machine Learning</li>
    <li><b>Part_5_2:</b> Machine Learning </li>
    <li><b>Part_6:</b> Evaluation of NADH Production After Enzyme Flux Modifications</li>
    <li><b>Part_7:</b> Introduction of HydABC Complex on iCH360 Model</li>
    <li><b>Part_8:</b> H₂ Production by Mutant Models</li>
    <li><b>Part_9:</b> Growth-coupled production of H₂ in the Models</li>
    <li><b>Part_10:</b> Dynamic Flux Balance Analysis (dFBA)</li>
    <li><b>Part_11:</b> Thermodynamic Analysis</li>
</ul>

## References
​​BEBER, Moritz E. et al. eQuilibrator 3.0: a database solution for thermodynamic constant estimation. Nucleic Acids Research, v. 50, n. D1, p. D603–D609, 7 jan. 2022. https://doi.org/10.1093/nar/gkab1106

CAO, Y., Liu, H., Liu, W., Guo, J., and Xian, M. (2022). Debottlenecking the biological hydrogen production pathway of dark fermentation: insight into the impact of strain improvement. Microbial Cell Factories, 21(1), 166. https://doi.org/10.1186/s12934-022-01893-3

​CORRAO, M., He, H., Liebermeister, W., Noor, E., and Bar-Even, A. (2025). A compact model of Escherichia coli core and biosynthetic metabolism. PLOS Computational Biology, 21(10), e1013564. https://doi.org/10.1371/journal.pcbi.1013564

​ORTH, J. D., Thiele, I., & Palsson, B. Ø. (2010). What is flux balance analysis? Nature Biotechnology, 28(3), 245–248. https://doi.org/10.1038/nbt.1614

​​SCHNEIDER, Philipp et al. StrainDesign: a comprehensive Python package for computational design of metabolic networks. Bioinformatics, v. 38, n. 21, p. 4981–4983, 31 out. 2022. https://doi.org/10.1093/bioinformatics/btac632

SCHUT, G. J., and Adams, M. W. W. (2009). The Iron-Hydrogenase of Thermotoga maritima Utilizes Ferredoxin and NADH Synergistically: a New Perspective on Anaerobic Hydrogen Production. Journal of Bacteriology, 191(13), 4451–4457. https://doi.org/10.1128/JB.01582-08
