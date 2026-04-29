# Presentation
<div style='text-align: justify'> Because of the intensive use of fossil fuels as the main energy source in modern society, mankind faces serious challenges against the consequences of the high amounts of greenhouse gas annually emitted. This way, much research has been conducted on the development of new sources of renewable energy, such as the utilization of biomass for H₂ generation through dark fermentation. Amidst the potential microorganisms capable of bioenergy production via fermentation, <i>Escherichia coli</i> stands out due to its position as a model organism, being highly described and utilized in different types of experiments. Furthermore, as a facultative anaerobic organism, <i>E. coli</i> metabolism shows great flexibility for metabolic engineering studies since it has the machinery for the metabolization of a large range of common compounds. </div><br>

<div style='text-align: justify'>However, regarding H₂ generation in <i>E. coli</i>, the native pathway leads to only 2 moles of H₂ per mole of glucose consumed, by the activity of pyruvate:formate lyase (PFL) (Reaction 1) and the formate:hydrogen lyase complex (Reaction 2):</div><br>

<p align="center">
pyruvate + CoA → formate + acetyl-CoA (Reaction 1)
</p>

<p align="center">
formate → H₂ + CO₂ (Reaction 2)
</p>

<div style='text-align: justify'>On the other hand, strict anaerobic species demonstrate high potential to synthesize biohydrogen through dark fermentation by the activity of specific hydrogenases, such as the hydrogenase ABC (HydABC) complex from the bacterium <i>Thermotoga maritima</i>, responsible for the transfer of e⁻ from NADH and reduced ferredoxin (Fd<sub>red</sub>) to protons H⁺ via an electron bifurcating mechanism. (Reaction 3).</div><br>

<p align="center">
Fd<sub>red</sub><sup>2−</sup> + NADH + 3H<sup>+</sup> → Fd<sub>ox</sub> + 2H₂ + NAD<sup>+</sup> (Reaction 3)
</p>

<p align="center">
ΔG° = +21 kJ
</p>

<div style= 'text-align: justify'> Therefore, as <b>suggested</b> by (Reaction 3), the HydABC complex could mediate the production of good amounts of H₂ if supported by enough concentration of NADH and Fd<sub>red</sub>, with emphasis on NADH, a very common cofactor present in a wide range of organisms. From the perspective of the pathways that lead to NADH generation, one can observe the tricarboxylic acid (TCA) cycle as a potential provider of the cofactor to the HydABC complex if operating on the reductive branch, since 3 moles of NADH are produced per turn of the cycle. Nevertheless, HydABC complex activity shows complete inhibition if in contact with even traces of O<sub>2</sub>, demanding the activity of the reductive branch under anaerobic conditions.</div><br> 

<div style='text-align: justify'> Accordingly, here, we provide a meticulous analysis of the capacity of biohydrogen production by the HydABC complex from <i>T. maritima</i> when heterologously expressed in the bacterium <i>E. coli</i>. To evaluate the maximum yield of H₂ production through the complex, the iCH360 genome-scale model will be used, serving as a basis to metabolic engineering simulations, such as flux balance analysis (FBA) and growth couple algorithms. Also, in the last steps of the analysis, the thermodynamics of H₂ synthesis by HydABC will be elucidated, taking into account the native pathways present in <i>E. coli</i> before the expression. Below are indicated the main objectives of the project: </div><br>

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
