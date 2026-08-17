Proceedings of the Estonian Academy of Sciences, 2020,**69**, 1, 57–73 [https://doi.org/10.3176/proc.2020.1.07](https://doi.org/10.3176/proc.2020.1.07) Available online at www.eap.ee/proceedings

# A brief tutorial overview of disturbance observers for nonlinear systems: application to flatness-based control

## Arvo Kaldmae¨ and Ulle Kotta ¨

Department of Software Science, Tallinn University of Technology, Akadeemia tee 21b, 12618 Tallinn, Estonia

Received 25 March 2019, accepted 19 June 2019, available online 13 February 2020

c 2020 Authors. This is an Open Access article distributed under the terms and conditions of the Creative Commons Attribution- NonCommercial 4.0 International License ([http://creativecommons.org/licenses/by-nc/4.0/](http://creativecommons.org/licenses/by-nc/4.0/)).

**Abstract.** The paper presents a brief overview of the most popular disturbance estimation techniques together with their application to flatness-based control. Two disturbance estimation approaches, the basic disturbance observer and the extended state observer, are described in a tutorial manner. Positive and negative aspects of both approaches are pointed out. Open research questions on disturbance estimation are presented. In the second part of the paper it is demonstrated how to integrate disturbance estimation into flatness-based control. The basic feedback linearization based approach, but also a novel event-based approach for differentially flat systems, are described. It is shown that disturbance estimation can be integrated easily into both of these control approaches. Finally, the results are demonstrated on three models: a heating, ventilation and air-conditioning; an active magnetic bearing; and an underwater vehicle models.

**Key words:** nonlinear control, disturbance estimation, flatness-based control, event-based control.

## 1. INTRODUCTION

Disturbances are inevitable part of almost any dynamical system. Since the behaviour of a disturbance in time is usually unknown and often the disturbance is unmeasurable, it causes a lot of trouble when designing controllers for the systems. Historically there exist two approaches to deal with disturbances. First, to design a robust controller, which yields in satisfactory performance even under the influence of the disturbances. Such control approaches are, for example: high-gain feedback; *H*¥control; passivity-based control; and sliding mode control. However, these approaches are robust, because they sacrifice some of the control performance. Second, to avoid the influence of the disturbance, a disturbance decoupling approach (see for instance [21,38]) is used. The goal here is to eliminate the influence of the disturbance from the system output to be controlled. The classical disturbance decoupling approach, unfortunately, is not always applicable. In the simple case of the single output it is important that the relative degree with respect to the disturbance would be strictly larger than the relative degree with respect to the control input. The latter is not necessary to solve the so-called almost disturbance decoupling problem [50], where the influence of the disturbance is not eliminated, but minimized. This, in turn, has similarities with robust control approaches, especially with the high gain feedback approach. However, there exists the third approach, which has become more and more popular in dealing with disturbances: the disturbance-observer-based

Corresponding author, arvo@cc.ioc.ee

*Proceedings of the Estonian Academy of Sciences, 2020,, 1, 57–73*

control (DOBC) [32]. The idea of this approach is to estimate the disturbance (and possibly a finite number of time-derivatives of the disturbance) and then integrate this estimate into some control approach. In this paper we address the DOBC approach. When disturbance decoupling is not possible and robust approaches are not good enough, it is natural to try to estimate disturbance signals. A historic overview of early results on disturbance estimation approaches is described in [22]. An overview of later developments can be seen, for example, in [10]. Over the years the disturbance estimation methods are called by many names: disturbance estimator, perturbation observer, extended state observer, disturbance observer etc. In this paper we refer to all of them as disturbance observers. Usually disturbance observers are studied in combination with DOBC. A positive aspect of DOBC, compared to the robust control approaches, is that when an estimate of the disturbance is used in the inner loop to compensate the effect of disturbance from system outputs, the performance of the outer loop controller is not degraded. That is why disturbance observers are integrated into some of the robust control methods, such as sliding mode control [49,54]. Also, the disturbance decoupling approaches have been studied in the DOBC framework using the disturbance observers [4,18,53]. In this paper the focus is on combination of disturbance observers with the flatness-based control approach. The flatness or feedback linearization-based control is very natural to combine with disturbance ob- servers. Flatness is a system property which allows to parametrize all system trajectories by the so-called flat output and its time-derivatives. This is true when the system model is exact and no external disturbances are present. If there are disturbances acting on the system equations, these disturbances (and possibly a finite number of their time-derivatives) affect directly the parametrization of the system trajectories. Therefore, by knowing how the disturbances affect the parametrization of the system trajectories, it is very easy to integrate disturbance observers to the basic flatness-based control. While flatness-based control approach can deal well with measurement noises, it is not, in general, robust against external disturbances and model uncer- tainties. Extending the flatness or feedback linearization-based control by integrating disturbance observers to the controller, one can increase the robustness of the approach. It is common that model uncertainties and external disturbances are integrated into one lumped disturbance vector, which is then estimated and used in the controller design. The goals of the paper are as follows. First, to give a short overview of some most popular methods to construct the disturbance observers for nonlinear control systems. The paper focuses on two approaches: the basic disturbance observer (BDO), first developed in [9], and the extended state observer (ESO). Both ap- proaches are described and then compared. Second, the paper demonstrates how the disturbance estimation can be integrated into the flatness-based control approach. We address the classical feedback linearization based approach, but also a novel event-based control approach, first introduced in [24], for differentially flat systems. Note that up to the knowledge of the authors it is the first time when disturbance observers are combined with an event-based control approach. Finally, the flatness-based control approaches combined with the ESO and the BDO, are simulated on three examples: on a heating, ventilation and air-conditioning system; an active magnetic bearing system; and on an underwater vehicle.

## 2. AN OVERVIEW OF DISTURBANCE OBSERVERS

A short overview of some popular methods of finding an estimate of a disturbance is provided. The strengths and weaknesses of various methods are discussed. Note that a fairly good overviews of disturbance observers for linear and nonlinear systems are already given in [8,10,37]. The paper [10] focuses on disturbance- observer-based control methods, but addresses briefly the disturbance estimation methods for linear and nonlinear systems. In [37] a nonlinear disturbance observer is constructed for Euler-Lagrange systems. However, the paper also contains a fairly good overview of disturbance observers is general. The objective of the paper [8] was to provide a historical viewpoint of the development of the so-called basic disturbance observer (see below), the disturbance observer-based control; and to present the link between the disturb- ance-observer-based control and nonlinear PID for a robotic manipulator under a number of assumptions. Our paper is meant to give a tutorial overview of the most popular approaches for disturbance estimation

*A. Kaldmae and ¨ U. Kotta: Tutorial overview of disturbance observers ¨*
**Table 1.** Overview of papers with different approaches for estimation of disturbance *w*

and assumptions made on disturbances

|||w(k)0|w(k)bounded|None|
|---|---|---|---|---|
|BDO|[7,40]|[9,52,55]|[16,45,56]|–|
|ESO|[13]|[31]|[2,19,41]|–|
|Sliding mode|[34]|–|[20]|–|
|Self-learning|–|–|[25,26]|–|
|Others|[17]|[28]|[3,12,48]|[1]|

<u>Disturbance dynamics known</u>

with a specific goal to apply these methods to improve the flatness-based control approaches. Note that the overview restricts the attention only on the brief exposition of the basic ideas of the approaches. Implemen- tation issues exceed the scope of this paper. However, it is worth pointing out that the paper [10] and the references therein discuss such aspects quite thoroughly. Disturbance observers are strongly connected to disturbance-observer-based control and in majority of cases, the two are studied together. That is, one does not only find the estimate of a disturbance, but also integrates the estimate to a controller design. Theoretical study of disturbance observers as a separate topic is not much advanced and most of the research is done towards specific applications [10]. For nonlinear disturbance observers there are two popular approaches: (1) the basic nonlinear disturbance observer (BDO) proposed, for example, in [7,9]; (2) the extended state observer (ESO) [2,19,31,41,48]. In the first case only the disturbance is estimated, though in general, the observer equations depend on system states and inputs. So a state observer is necessary unless all the states are measurable. The idea of the ESO is to extend the original state vector by the disturbance vector and possibly, some of its time-derivatives, and then design a state observer for the extended system. There are also other types of disturbance observers, like, sliding- mode-based [20,34], fuzzy [30], self-learning [25,26] and other specific [1,3,12] disturbance observers. In this paper we focus mostly on the BDO proposed in [9] and on the ESO. The reason for such choice is twofold. First, these are most popular approaches in the literature and second, they allow to estimate also the time-derivatives of the disturbances. The latter is especially important in integrating disturbance observers into the flatness-based control approach. Another way of classifying the nonlinear disturbance observers is by the assumptions made on the dis- turbance. Some papers [7,13,31,34,40,49] assume that the disturbance dynamics is known, other papers assume that the disturbance and/or some of its time-derivatives are bounded [2,16,41]. It is often assumed that the first [9] or some higher order [28,55] time-derivatives of the disturbance are approximately zero. The assumption that the disturbance dynamics is known or the disturbance is generated by certain, usu- ally linear, dynamics, means in practical terms that the incomplete system model is just improved. When time-derivatives of the disturbance are assumed to be bounded, then most one can prove is that the error dynamics (real minus the estimated disturbance) is also bounded. Obviously, the assumption that the first time-derivative of the disturbance is approximately zero works well for constant or very slowly varying dis- turbances. This limits applicability of this type of disturbance observers. A much weaker assumption is that the *k*th order time-derivative of the disturbance is approximately zero. In principle, this assumption allows to estimate all the disturbances, which behave as an analytic function on some (long enough) time-interval, since such functions can be approximated by a polynomial on the given time-interval. An overview of dif- ferent approaches for disturbance estimation based on the assumptions made on the disturbance *w* are given in Table 1.

## 2.1. Basic disturbance observer

Consider a control-affine system of the form

*x*˙ = *f* (*x*) +*g₁*(*x*)*u* +*g₂*(*x*)*w;* (1)

where *x*(*t*) R *n* is the state, *u*(*t*) R *m* is the input and *w*(*t*) R *r* is the disturbance of the system. A disturbance observer was proposed in [9] to estimate the disturbance *w* in (1) under the assumption that *w*˙ = 0. The observer equations are as follows:

*z*˙ = *L*(*x*)[*f* (*x*) +*g₁*(*x*)*u* +*g₂*(*z* + *p*(*x*))]*;*

(2)
*w*ˆ = *z* + *p*(*x*)*;*

where *z*(*t*) *2* R *r* is the observer state, *w*ˆ (*t*) is the estimation of the disturbance *w*(*t*), *p*(*x*) and *L*(*x*) are the observer gains to be chosen, satisfying

<u>¶ p(x)</u> *L*(*x*) = *:* (3) *¶ x*

It has been shown that the error *e* = *w w*ˆ dynamics is

## e˙ = L(x)g₂(x)e:

Now, the gain *L*(*x*) must be chosen such that the error dynamics is stable for every *x* and *p*(*x*) is computed from (3). A systematic way of choosing *L*(*x*) is described in [9] for a multilink robotic manipulator. Note that in order to apply the disturbance observer (2), one has to assume that the system state *x* and input *u* are known. The disturbance observer (2) was quickly generalized for the case when the disturbance was generated by a linear dynamics [7], in which case the assumption *w*˙ = 0 was not needed anymore. Also an approach to choose the gain values *L*(*x*) was given in [7]. The approach has become popular in many applications, see for instance [37,52]. The paper [55] tried to generalize the approach for the case when a higher order time-derivative of the disturbance was assumed to be zero, but is shown to be incorrect [23]. In fact, the correct generalization was already proposed in [16] and later in [6,45,56]. All these results consider the case when the disturbance enters the system dynamics linearly, i.e. the case when *g₂*(*x*) is constant or even identity matrix. The paper [16] also assumes the nominal system to be in the Brunovsky canonical form. An important property of the generalized basic disturbance observer is that it also gives estimates of the time-derivatives of the disturbance. Here we give the generalized basic disturbance observer for a more general class of systems (1). Assume now that the *k*th time-derivative of *w* is zero, i.e., *w*

(*k*) = 0. Then, the disturbance observer (2) is generalized
to *z*˙ 0= *L₀*(*x*)[*f* (*x*) +*g₁*(*x*)*u* +*g₂*(*z₀*+ *p₀*(*x*))] +*z₁*+ *p₁*(*x*)*;* *z*˙ 1= *L₁*(*x*)[*f* (*x*) +*g₁*(*x*)*u* +*g₂*(*z₀*+ *p₀*(*x*))] +*z₂*+ *p₂*(*x*)*;* ... *z*˙ *k* 2= *Lk* 2(*x*)[*f* (*x*) +*g₁*(*x*)*u* +*g₂*(*z₀*+ *p₀*(*x*))] +*zk* 1+ *pk* 1(*x*)*;* *z*˙ *k* 1= *Lk* 1(*x*)[*f* (*x*) +*g₁*(*x*)*u* +*g₂*(*z₀*+ *p₀*(*x*))]*;* (4) *w*ˆ = *z₀*+ *p₀*(*x*)*;* *w* ˆ˙ = *z₁*+ *p₁*(*x*)*;* ...

*w* \ (*k* 1) = *zk* 1+ *pk* 1(*x*)*;*

where for *i* = 0*; : : :; k* 1, *zi*(*t*) *2* R *r* is the observer state, *w* d(*i*) is the estimation of *w*

(*i*), *pi*(*x*) and *Li*(*x*) are
observer gains to be chosen, satisfying

<u>¶ pi(x)</u> *Li*(*x*) = *:* (5) *¶ x*

Now, let *ei*:= *w*

(*i*) *w* d(*i*), *i* = 0*; : : :; k* 1. Then, under the assumption *w*
(*k*) = 0, one has
*e*˙ 0= *e₁ L₀*(*x*)*g₂*(*x*)*e₀;* *e*˙ 1= *e₂ L₁*(*x*)*g₂*(*x*)*e₀;* ..

. (6)
*e*˙ *k* 2= *ek* 1*Lk* 2(*x*)*g₂*(*x*)*e₀;* *e*˙ *k* 1= *Lk* 1(*x*)*g₂*(*x*)*e₀:*

Choosing *Li*(*x*), *i* = 0*; : : :; k* 1, such that dynamical system (6) is stable for all *x* guarantees that *ei*, *i* = 0*; : : :; k* 1, stabilizes to zero. Then, *pi*(*x*) can be found from (5). To guarantee the stability of (6) for all

||||n r|r n|
|---|---|---|---|---|
|||||i|

values of *x* is not, in general, a simple task. However, if *g₂*(*x*) *2* R *n r*, then one can also choose *Li*(*x*) *2* R *r n*

for *i* = 0*; : : :; k* 1. Then the error system (6) becomes a linear autonomous system and the gains *L*, *i* = 0*; : : :; k* 1, can be found such that the roots of the characterizing polynomial of the state transition matrix are on the left-half of the complex plane.

## 2.2. Extended state observer

The basic disturbance observer (2) and the generalized disturbance observer (4) depend on the knowledge of the system state *x* and the input *u*. The extended state observer (ESO) can be used to estimate the disturbance under the same assumptions, i.e., *w*˙ 0 or *w*

(*k*)
0. However, the ESO does not need the knowledge of the
system state *x*, but also provides estimates of the state variables. Consider the system (1) and assume that *w*

(*k*) 0 for some *k 2* N. Extend the state vector of system (1)
to ¯*x* = (*x; w; w*˙*; : : :; w* (*k* 1) ) *T*, which yields the extended system equations

*x* ˙¯ = *f*¯(*x*¯) +*g*¯ 1 (*x*¯)*u:* (7)

Now, the state *x*, the disturbance *w* and its first *k* 1 time-derivatives *w*

(*i*), *i*= 1*; : : :; k* 1, for system (1) can
be estimated by constructing an observer for the extended system (7). Like in the basic disturbance observer case, one can, instead of *w*

(*k*) 0 assume that the dynamics of the disturbance is known and extends the
system accordingly. Essentially, the state extension based methods rely (sometimes implicitly) on the property that *the ex-* *tended system* (7) *is observable*. This can at times be a restrictive assumption. For instance, consider the simple linear system *x*˙ 1= *x₂*+*d₁;* *x*˙ 2= *u* +*d₂;* (8) *y* = *x₁*

and extend it with the dynamics of the disturbance

*d* ˙ 1= 0*;* *d* ˙ 2= 0*:*

(9)
It is easy to check that the system (8)–(9) is not observable since observability matrix has rank three whereas the number of extended states is four. Thus the disturbance vector to be added to nominal plant equations is limited to the one with dimension 1. Even more, system (8)–(9) with *d₂* = 0 is still not observable. How- ever, the case with *d₁* = 0 is observable. This situation corresponds to the so-called matched disturbance case when the disturbance input does not show up earlier on the output than the control input. Therefore, ap- plicability of ESO methods is limited and often scalar disturbances are considered [31]. A bit less restrictive

is the case when the disturbance dynamics is assumed to be known. However, the observability assumption is still necessary. If we assume that the disturbances in the system (8) are generated by the model

*x* ˙ 1= *x ;*2 *x* ˙ 2= 0*;* (10) *d₁* = *x₁;* *d₂* = *x₂;*

then one still cannot observe *x₁*, *x₂*, *x₁* and *x₂* from the output *y* and its time-derivatives. Different approaches have been used to find the state observer for the extended system. In [2,31] the standard Luenberger observer is constructed, while in [19,41,48] more advanced observers are used.

## 2.3. BDO versus ESO

In this subsection we discuss advantages and disadvantages of both, the basic disturbance observer (BDO) and the ESO. The common feature of both is the assumption made for the disturbance: either a time- derivative of the disturbance is assumed to be zero or the dynamics of the disturbance is assumed to be known. Now, we compare both methods with respect to their applicability.

1. First, to apply the BDO, the system state and input have to be known, whereas it is not required to apply the ESO. However, observability assumption of the extended system is needed in case of the ESO. Under the assumption that the full state vector *x* is measured, the two methods are both applicable, since then the extended system (7) is always observable. However, if this is not the case, the ESO can still be applied (under the assumption that the extended system (7) is observable), but the BDO, in general, cannot be used.
2. Second, choosing the gains *Li*(*x*) in BDO can be difficult if *g₂*(*x*) is highly nonlinear. If the disturbance is added in the system equations linearly, as often assumed in applications, then the gains *Li*(*x*) can be chosen constants and the stability of the error dynamics can be easily guaranteed. The problematic aspect of the ESO may be construction of the observer for the extended system (7). The reason is that the extended system (7) can be highly nonlinear and observer construction for such systems is not a trivial task. Then again, under the assumptions that all the state variables are measurable and the disturbance is added in the system equations linearly, the extended system (7) is in the observer form, for which an observer can be easily constructed.
3. Third, the BDO has been developed for disturbance affine systems, whereas, in principle, the ESO can be used for general nonlinear systems, where the disturbance enters into the system dynamics in non- affine manner. Summarizing, under the same assumptions (the state vector *x* is measured and the disturbance is added linearly), the BDO and ESO are approximately equally effective. However, the ESO can be, in general, applicable for non-affine systems, while the BDO does not. It is still worth pointing out that constructing the observer for the extended system in a non-affine case is a difficult problem itself. Although we have assumed that in both cases – the BDO and the ESO – the *k*th time-derivative of the disturbance *w* is zero, both methods succeed also when the assumption is not exactly satisfied. The assumption was made primarily to guarantee the asymptotic stability of the error dynamics. Note that the error dynamics can still be stable in the sense that *jje*(*t*)*jj < e*, if the *k*th time-derivative of the disturbance is assumed to be just bounded. Additionally, the value of *e* can be lowered by choosing the higher gain values.
## 2.4. Other approaches

This subsection contains a brief discussion of some other approaches for the design of disturbance observers, developed during the past few years.

The paper [1] relies on the concept of tracking differentiators to define nonlinear disturbance observers. The approach has similarities with the ESO. Instead of assuming that the time-derivative of the disturbance is zero, the time-derivative of the disturbance is assumed to be generated by a tracking differentiator. The authors claim that their disturbance observer can estimate almost all types of disturbances and does not need any prior information about the disturbance. Nevertheless, the applicability of the approach remains questionable, since only scalar systems (*n* = 1) were studied and no hint was given how to generalize the approach for non-scalar case. Also, it seems that the knowledge on the state and input variables is necessary. A totally different approach is presented in [12]. A *specific matched disturbance*, which affects directly the input, is considered. Then the Hirschorn (left) inverse of the control system is used to compute the estimate *v*ˆ of the total input *v* := *u* + *w*. Since the inverse depends on the system states, a separate state estimation is necessary. Then, *v*ˆ is compared to the input *u* to receive an estimate of the disturbance *w*. Low-pass filters are also used to estimate the time-derivatives of the output. Finally, in [3] a state observer is constructed for systems with bounded exogenous inputs (disturbances and sensor noise). Then an unknown input is estimated based on the observed and measured state variables. However, only systems with specific structure and linear disturbances are considered.

## 2.5. Future research

A number of future research directions are named in [10] concerning disturbance (and uncertainty) estima- tion and attenuation. As mentioned in [10], the theoretical research is still well behind the applications in this research area. Many methods for disturbance estimation assume that the system state is measurable (for example BDO). Also, most approaches are developed for control- and disturbance-affine systems or even for systems with linear disturbances. Regarding the above restrictions the ESO is an exception; however, the observer construction in such case may become very difficult if possible at all, since it requires constructing an observer for a general nonlinear control system. Finally, note that only a few papers [5,27,44] study disturbance observers for discrete-time systems. An ESO was developed in [5] for linear discrete-time systems under the assumption that the disturbance is slowly varying compared to the sampling time. The BDO was generalized in [27] to linear discrete-time systems. Moreover, another observer, similar to the BDO, was given in [27] to relax the assumption that all the states are available for the measurement. These results were further developed in [44].

## 3. FLATNESS-BASED CONTROL

In this section we describe the basic flatness-based control approach as well as a novel event-based con- troller for differentially flat systems. The estimates of disturbances and possibly their time-derivatives are incorporated to both controllers. The flatness-based control with disturbance observers has been used before in [17,25,47]. Note that for mismatched disturbances the estimates of some time-derivatives of the disturb- ance are necessary, whereas for matched disturbances it may not be necessary. Incorporation of disturbance observers into these control schemes is not strictly necessary, but helps to improve the performance while keeping control values smaller, which in many applications corresponds to lower energy usage. Consider a nonlinear control system of the general form

*x*˙ = *f* (*x; u*)*;* (11)

where *x*(*t*) *2 X* R *n* is the system state and *u*(*t*) *2 U* R *m* is the system input. It is assumed that the function *f* is analytic and satisfies on some open and dense subset of *X U* the condition rank[*¶ f =¶ u*] = *m*, meaning that there are no redundant inputs. Recall the flatness property of system (11) as follows [29].

**Definition 1.** *System* (11) *is said to be flat if there exists an output function*

*y* = *h*(*x; u; : : :; u*

(*l*)
) *l* 0 (12)
(*y*(*t*) *2* R *m* )*, called flat output, such that*

||x|(k)|
|---|---|---|
|x u|u|(k+1)|

*x* = *j* (*y; : : :; y*)*;* (13)

*u* = *j* (*y; : : :; y*) (14)

*for some k 2* N *and functions j, j.*

A more formal definition of flatness and more thorough discussion can be found, for example, from [14,15,29]. The flatness-based control has attracted a lot of attention throughout last decades, see the books [29,43]. It is known that any differentially flat system is also feedback linearizable by an endogenous state feedback. However, often disturbances affect the equations (11), i.e., one has

*x*˙ = *f* (*x; u; w*)*;* (15)

for the disturbance *w*(*t*) *2* R *r*. In this case the relations (13) and (14) are also affected by the disturbance and some finite number of its time-derivatives, i.e.,

|x|(k)|(m )|
|---|---|---|
|u|(k+1)|(m +1)|

*x* = *j*˜ (*y; : : :; y; w; : : :; w*)*;* (16)

*u* = *j*˜ (*y; : : :; y; w; : : :; w*)*:* (17)

When the disturbance and its time-derivatives are not known or estimated, then the nominal model (11) and corresponding relations (13), (14) are used in the control design. If the disturbance and its time-derivatives are estimated, then one can use the more accurate relations (16) and (17) instead.

## 3.1. Feedback linearization based control

To simplify the situation, consider a single input system (11) with *y* = *h*(*x*) being the flat output. Then, replace *y* and its first *k* time-derivatives in (14) (or (17)) by *h*(*x*) and its first *k* time-derivatives and *y* (*k*+1) by a new control input *v*. This gives us the feedback

*u* = *ju*(*h*(*x*)*; : : :; h*

(*k*)
(*x*)*; v*)
or *u* = *ju*(*h*(*x*)*; : : :; h*

(*k*)
(*x*)*; v; w; : : :; w*
(*m*+1) )

respectively, which yields a linear closed-loop system *y* (*k*+1) = *v*. Now, any linear control approach can be used to control the closed-loop system. For example, one can take

||(k+1) ki=0|i (i)|(i)|
|---|---|---|---|
||i|||
|k (k)||||

*v* = *r q* (*y r*)*;* (18)

where *r*(*t*) is the reference trajectory of *y* and *q* R, *i* = 0*; : : :; k*, are chosen such that the error *e* = *y r* dynamics *e* (*k*+1) + *q e* + +*q₀e* = 0 is stable.

## 3.2. An event-based approach

A different, an event-based, approach for controlling differentially flat systems is briefly described in this subsection. Assume for simplicity that the flat output y = h(x) is also the output-to-be-controlled of system (11). Here, instead of replacing y =(y₁,...,ym) T and its time-derivatives in (14) (or (17)) by h(x) and its time-derivatives, we replace y =(y₁,...,ym) T and its time-derivatives by a pre-defined trajectories

y ir(t)=pi(t)e −Kit + ri(t), i = 1,...,m, (19)

which converge to the desired trajectories ri(t) of yi, i = 1,...,m. The polynomial pi(t) ∈ R[t] is used to match the actual initial conditions of the system states and desired initial states, i.e., to guarantee that

(k)
x(0)=*ϕ*x(yr(0),...,yr(0)), (k+1) (20) u(0)=*ϕ*u(yr(0),...,yr(0)),

where yr=(y1r,...,ymr) T. Finally, the constant parameters Ki, i = 1,...,m, can be freely chosen and affect the speed at which the output yirconverges to the desired reference trajectory ri(t). Then one gets a feedforward controller

(k+1) u = *ϕ*u(yr,...,yr)

or (k+1) (*μ*+1)
u = *ϕ*u(yr,...,yr, w,...,w),

which directs the system output y to follow the trajectory yr. Because uncertainties and disturbances affect the system, the actual output trajectory starts to deviate from the desired one yr. If this happens, an event is generated and a new desired trajectory yris computed based on the actual measurements of the system
states. Since yralways converges to r =(r₁,...,rm), then, if Ki, i = 1,...,m, are appropriately chosen, y
also converges to r.

## 4. EXAMPLES

In this section we demonstrate on three examples from different areas how the flatness-based control together with disturbance estimation improves the system performance compared to the case when no disturbance estimation is used. Also, up to the authors knowledge, this is the first time when disturbance observers are integrated into an event-based control approach. Doing so we not only improve the performance of the closed-loop system, but also reduce the number of events necessary to achieve such closed-loop per- formance. The number of events, in turn, corresponds to communication load between the sensors and the controller. First, an ESO is constructed to estimate a slowly varying unmeasured thermal load acting on a heating, ventilation and air-conditioning (HVAC) model. Second, a very fast disturbance and its time-derivative are estimated to control an active magnetic bearing system. We show that although the assumptions of the generalized BDO (4) are not satisfied (second derivative is not approximately zero) the observer (4) can still be used to estimate the disturbance and its derivative. Third, a BDO is constructed to estimate disturbances acting on an underwater vehicle and integrated to the event-based controller, described in Subsection 3.2.

## 4.1. Heating, ventilation and air-conditioning system

A model of heating, ventilation and air-conditioning system (HVAC) was given in [35] for one thermal zone as follows:

||c|
|---|---|
|1|C s|
|2|C11R|

p x˙ = (T − x₁)u + C1R (x₂ − x₁)+ C 1R (To− x₁)+w, 1 1 1 o x˙ = (x₁ − x₂), (21) 2 y = x₁, where the system variables and parameters are described in Table 2.

**Table 2.** Descriptions of different variables and parameters in model (21)

Physical description

|Symbol|Value|||
|---|---|---|---|
|x1|State variable|Air temperature of the thermal zone||
|x2|State variable|Temperature of floors, walls, furniture etc.||
|u|Input variable|Mass flow rate of supply air||
|w|Disturbance variable|Unmeasured thermal load||
|cp|0.000281, kWh/kg*K|Heat capacity of thermal zone air||
|C1|0.00275, kWh/K|Thermal capacitance of air||
|C2|1.87733, kWh/K|Thermal capacitance of floors, walls, furniture etc.||
|Ts|17,oC|Temperature of supply air||
|R|2.08, K/kW|Thermal resistance between C|1and C2|
|Ro|11.849, K/kW|Thermal resistance between the thermal zone and outside air||
|To|27,oC|Outside air temperature||

We want to estimate *w*. Assuming that *w*˙ = 0, we extend the equations (21) with *x₃* = *w*, which yields an extended system

*x*˙ = *Ax*+ *g*(*y; u*)*;* (22) *y* = *x₁;*

where 0 1

|1 1|1|
|---|---|
|C R C R|C R|
|C1R|C1R|

1 1 *o* 1 1 *A* = @ 0 A 2 2 0 0 0

and 0<u>c</u> <u>p T</u> 1 (*T y*)*u* + <u>o</u> *:* *C*1*s C*1*Ro* *g*(*y; u*) = @ 0 A *:* 0

System (22) is observable and moreover, in the observer form, thus one can construct an observer

*x* ˙ˆ = *Ax*ˆ +*g*(*y; u*) +*L*(*y x*ˆ₁)*:* (23)

Let the error be *e* = *x x*ˆ, then the error dynamics becomes

*e*˙ = (*A LC*)*e;*

where*C* = (1 0 0). The matrix *L* = (*l₁ l₂ l₃*) *T* can be chosen such that *A LC* is an asymptotically stable matrix. The estimate ˆ*x₃* of (23) gives the estimate of *w*. In model (21) we want to control the room temperature *x₁*. Note that, *x₁* is not the flat output of the system. Instead, *y* = *x₂* can be chosen as the flat output. Therefore, using the feedback linearization based control approach we can only control directly the variable *x₂*. Nevertheless, from the second equation of (21), by driving *x₂* to a constant value, the variable *x₁* will achieve the same constant value. The goal is to change room temperature *x₁* from 27 o C to 20 o C when outside temperature is 27 o

C. The simulations in
Fig. 1 show that the observer (23) tracks the disturbance and that the feedback linearization control approach

is much improved compared to the case when no disturbance estimation is added to the controller.

||A. Kaldmae and ¨|¨|||U. Kotta: Tutorial overview of disturbance observers|||||||||67|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|(a) (a)|(a) 3 3 2 2||||disturbance disturbance disturbance estimate disturbance estimate||(b) (b) C]C] o o, °C (ºC) [[ 1 x|(b) 30 30 25 25 20 xx 11 20|||||without disturbance estimation without disturbance estimation with disturbance estimation with disturbance estimation||
||1 1 ww|||||||15 15 0 0|5 5|10 10|||15 20 15 20||
||0 0||||||C]C] oo, °C (ºC) [[ 2 x|30 30 25 25 20 xx 22 20|||||||
||-1 -1 0 0|5 10 5 10||t (h) t, h t [h] t [h] Figure 1. Figure 1. Fig. 1.|15 20 15 20||The disturbance (a) and state variables (b) for system (21). The disturbance (a) and state variables (b) for system (21). The disturbance (a) and state variables (b) for system (21).|15 15 0 0|5 5|10 10|t, h t [h] t [h]|t (h)|15 20 15 20||
|φ₁ − where|4.2. Active the dynamics where x₁ φ₂ Moreover, Table 3.|is the rotor position [m], x₂, where φ₁ and φ₂ 1mA ϑ₁ =, ϑ₂ μ 0 earization approach, we design the controller|magnetic bearing system|−2Ns = μ 0 The flat output of system (24) can be chosen as y₁ u₁ u₂|x˙ = 1 = x˙ 2 = x˙ 3 x˙ = 4 y = R 2NR 02 and ϑ₃ 2 A μ 0 v 1 = N(ϑ x 1 4 = N(v₂ − = −q₁₂ y¨ v₁ = −q₁₂ (|A voltage-controlled model of an active magnetic bearing (AMB) system is given in [36] and described by x₂, ϑ₁ x₃ x₄ 1 u₁ + N 1 u₂ + N x₁, is the rotor speed [m/s], x₃ A − ϑ₂ x₃ − ϑ₂ x₄ − ϑ₃ − q₁₁ y˙ 1 1 ϑ₁ x₃ x₄ + re f|1 + m ϑ₂ x₃ ϑ₂ x₄ ϑ₃ x₁ x₁ − q₁₀ 1 m|w, + ϑ₃ + ϑ₃ = x₁ x₄ x₃), y₁ w) − q₁₁|x₁ x₄, x₁ x₃, = φ, x₄ b are the electromagnetic fluxes [Wb] of two opposite electromagnets, respectively. and y₂ = x₄. xx v w˙ x 3 2 − − m ϑ 4 1 4 x₂ − q₁₀ x₁,|= are known constants, with system parameters described in),|φ c|, for|φ = φ₁ + φ₂, φ c b According to the feedback lin-|(24) = (25) (26)|
|q₁₂ and L₁||The parameters q 1 j = 120 and q₂₀ = 40. ance estimation. Thus, from (5) one has p₀|||v₂ = −q₂₀ (y₂, j = 0, 1, 2, and q₂₀ In the current simulations we want the convergence to be fast, so we choose q₁₀|− y₂ time-derivative w˙. To estimate them, we use the BDO approach, described in Subsection 2.1. The disturbance observer (4) is constructed under the assumption that w¨ = 0. We choose L₀ (x)=500x₂|=(0, 16000, 0, 0), which yield stable error dynamics (6) and fast enough convergence of the disturb-, p₁|)=−q₂₀|(x₄ − 0.001). are chosen such that the linearized system equations are stable. Note that the controller (25), (26) depends on the disturbance w and its first (x)=16000x₂||||= 64000, q₁₁ = 4800, =(0, 500, 0, 0), and the disturbance observer||

|68 68|||||||||Proceedings of the Estonian Academy of Sciences, 2020, Proceedings of the Estonian Academy of Sciences, 2020,|69 69|, 1, 57–73, 1, 57–73|
|---|---|---|---|---|---|---|---|---|---|---|---|
|(¨||||1 Table 3. z˙ = 500[ϑ₁ x x + (z₀ 0 3 4 m 1 = −16000 [ϑ x x + z˙ 1Symbol 3 4 m Value¹ wˆ s = z₀ + 500 x₂,, m 0.0004 Air gap 0 + 16000 x₂. wˆ˙ m, = z₁ kg 2.5, H 0.0025 L o L, H 0.0005 ˆ˙ are integrated to controller (25), (26). s Now, the estimates wˆ and w R, Ω 0.5 as a sinusoid with constant frequency and amplitude. N 108 disturbance and its time-derivative together with their estimates is presented. Note that since the assumption − 6 μ, H/m 1.25 × 10 0 w = 0) made in the disturbance observer construction is not actually satisfied, the error does not converge 2 A, m 0.0014 to zero, but is bounded around zero. Figure 2b presents the state variables of the closed loop system in two k, N/A 15.625 i cases: when the feedback linearization based control is combined with the disturbance observer (27) and k, N/m 97656.25 s when it is not. Clearly, the addition of disturbance observer to the controller improves the performance of the closed-loop system significantly.||−Values and descriptions of AMB system parameters 0 Mass of the rotor Coil inductance Coil resistance Current stiffness|Coil inductance losses|+ 500x Permeability of free space Displacement stiffness|+ 500x)] + z + 16000x, 2 1 (zPhysical description)], 2 Number of turns of wire in the coil Cross sectional area of air gap|2 The actual disturbance is simulated Figure 2 shows the simulation results. In Fig. 2a the|(27)|
|(a)|(a) models.|(a) w w w -1 60 60 40 40 20 20 dw/dt dw/dtdw/dt|(a) 11 00 -1 00 00|the AMB system where a disturbance observer is integrated into the control scheme. ([11,33,39,40,46]) consider linear voltage-controlled models, 1 1 Also, different methods for disturbance estimation are being used. 0.8 0.8 46], the ESO [33,51] or inversion-based method with low-pass filters [39]. 0.6 0.6 approaches are implemented, such as flatness-based-control [17], a linear state feedback [40,46], an output 0.6 0.65 0.7 0.6 0.65 0.7 0.2 0.4 0.6 0.8 11 1.2 1.4 1.6 1.8 22 0.2 0.4 0.6 0.8 1.2 1.4 1.6 1.8 actual disturbance actual disturbance disturbance estimate Table 3. disturbance estimate Symbol Value|Note that there are many papers (for example, [11,17,33,39,40,46,51]) that present results on controlling (b) (b)|2 2 x x x Values and descriptions of AMB system parameters|1 1 1 x x x 0.01 2 -0.01 3 33 x x x 44 4 x x|(b) (b) 55 0 0 -5 -500 0.01 0 0 -0.01 00 11 00 -1 -1 22 1 1|-4-4 10 10 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 -5 10 -5 10 00 10 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 -3-3 10 Physical description|Some of the papers others [17,51] nonlinear current-controlled For example, the BDO [40, 11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 Moreover, different control 11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 without disturbance estimation without disturbance estimation with disturbance estimation with disturbance estimation|22 22 22|
||Figure 2. Fig. 2. Figure 2.|-20|-2000|s, m 0.0004 Air gap 0 0.2 0.4 0.6 0.8 11 1.2 1.4 1.6 1.8 22 0.2 0.4 0.6 0.8 1.2 1.4 1.6 1.8 2.5 ttm, kg, H 0.0025 L o. (a) Disturbance ww, its time-derivative w (a) Disturbance w, its timederivative ẁ (a) Disturbance, its time-derivative w L, H 0.0005 s no disturbance estimation added to the control design. disturbance estimation added to the control design. no disturbance estimation added to the control design. R, Ω 0.5 N 108 − 6 μ₀, H/m 1.25 × 10 2 A, m 0.0014 1 z˙ = −500[ϑ₁ x₃ x₄ + (z₀ 0 m k, N/A 15.625 i 1 = −16000[ϑ₁ x₃ x₄ + z˙ 1 m k, N/m 97656.25 s wˆ = z₀ + 500x₂, + 16000x₂. wˆ˙ = z₁|(z₀|Mass of the rotor Coil inductance Coil resistance Current stiffness|x Coil inductance losses + 500x₂|0 000 Permeability of free space Displacement stiffness|0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 ˙˙ and their estimate; (b) The state trajectories compared to the case when there is and their estimate; (b) The state trajectories compared to the case when there is no and their estimate; (b) The state trajectories compared to the case when there i Number of turns of wire in the coil Cross sectional area of air gap)] + z₁ + 16000x₂ + 500x₂)],|11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 tt,|22 s (27)|
|(a)|(a)|(a)|(a)|Now, the estimates wˆ and wˆ˙ are integrated to controller (25), (26).|(b) (b)|||(b) (b)|-4|The actual disturbance is simulated||
|||0 w|11|as a sinusoid with constant frequency and amplitude. 1 1 disturbance and its time-derivative together with their estimates is presented. Note that since the assumption 0.8|||1 1 1 x x x|55 0 0 -5 -5|10 -4 10 Figure 2 shows the simulation results.|In Fig. 2a the||
|(¨|dw/dt|w w -1 60 60 40 40 20 20 dw/dt 0 dw/dt|0 -1 0 0 when it is not. 0|0.8 w = 0) made in the disturbance observer construction is not actually satisfied, the error does not converge 0.6 0.6 0.6 0.65 0.7 to zero, but is bounded around zero. Figure 2b presents the state variables of the closed loop system in two 0.6 0.65 0.7 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8 2 cases: when the feedback linearization based control is combined with the disturbance observer (27) and actual disturbance actual disturbance disturbance estimate the closed-loop system significantly. disturbance estimate the AMB system where a disturbance observer is integrated into the control scheme.|Note that there are many papers (for example, [11,17,33,39,40,46,51]) that present results on controlling|22 2 x x x|0.01 -0.01 3 3 3 x x x 44 4 x x|00 0.01 00 -0.0100 11 Clearly, the addition of disturbance observer to the controller improves the performance of 0 0 -1 -1 00 2 2 11|0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 -5 10 -5 10 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 -3-3 10 10|11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 11 1.2 1.4 1.6 1.8 1.2 1.4 1.6 1.8 without disturbance estimation without disturbance estimation with disturbance estimation with disturbance estimation Some of the papers|22 22 22|
||models. 46], Figure 2. Fig. 2. Figure 2.|-20|-2000|0.2 0.4 0.6 0.8 11 1.2 1.4 1.6 1.8 22 ([11,33,39,40,46]) consider linear voltage-controlled models, 0.2 0.4 0.6 0.8 1.2 1.4 1.6 1.8 tt Also, different methods for disturbance estimation are being used.. the ESO [33,51] or inversion-based method with low-pass filters [39]. (a) Disturbance ww, its time-derivative ww (a) Disturbance w, its timederivative ẁ (a) Disturbance, its time-derivative no disturbance estimation added to the control design. disturbance estimation added to the control design. approaches are implemented, such as flatness-based-control [17], a linear state feedback [40,46], an output no disturbance estimation added to the control design.|||x|0 000|0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 ˙˙ and their estimate; (b) The state trajectories compared to the case when there is and their estimate; (b) The state trajectories compared to the case when there is no and their estimate; (b) The state trajectories compared to the case when there i|11 1.2 1.4 1.6 1.8 others [17,51] nonlinear current-controlled 1.2 1.4 1.6 1.8 tt For example, the BDO [40, Moreover, different controls|22|

A. Kaldm A. Kaldmae and ¨ae and ¨ U. Kotta: Tutorial overview of disturbance observers U. Kotta: Tutorial overview of disturbance observers ¨¨ feedback control law [51], H∞control [39] etc. However, up to the authors knowledge, there are no papers,
**Table 4.** Values of the parameters for U-CAT model
 where a disturbance-observer-based control method is applied to a nonlinear voltage-controlled model, such
Parameter Value Parameter Value as (24). C –40 C 59

|C1|–40|C2|59|
|---|---|---|---|
|C3|59|C4|40|
|C5|–19|C6|2.8179|
|Xuu Nrr|56 0.7226|Yvv|551|

1 2

## 4.3. Underwater vehicle

A model of an underwater vehicle, called U-CAT, is proposed in [42]. It has two motion modes, denoted by SLOW and FAST, which depend on how the four fins of the vehicle are configured. The state space model feedback control law [51], H∞control [39] etc. However, up to the authors knowledge, there are no papers, for SLOW mode is as follows: where a disturbance-observer-based control method is applied to a nonlinear voltage-controlled model, such as (24). x˙ = x cos (x ) − x sin (x ), 1 2 5 4 5 x˙ 2= − C C 1 x₄x₆− XC uu x₂|x₂| + C u 1 + w₁, 2 2 1 x˙ 3= x₂ sin (x₅)+x₄ cos (x₅),

## 4.3. Underwater vehicle

x˙ = − C3 x x − Y vv x |x | + u 2 + w, (28) 4 C 4 2 6 C 4 4 4 C 4 2 x˙ 5= x₆, A model of an underwater vehicle, called U-CAT, is proposed in [42]. It has two motion modes, denoted byC5Nrru3 x˙ 6= −Cx x2 4−Cx |x | +6 6 C+ w ,3 SLOW and FAST, which depend on how the four fins of the vehicle are configured. The state space model6 6 6 for SLOW mode is as follows: T where w =[w₁, w₂, w₃] represents the unknown disturbance vector. The parameter values of the model (28) are displayed in Table 4. x˙ 1= x₂ cos (x₅) − x₄ sin (x₅), The flat outputs of the system (28) are chosen as x˙ 2= − C1 x₄x₆ − y XC1 uu= x₂x|x₁₂,|y+2= u 1x+3, and w₁, y₃ = x₅, which we also want to C2 2C1 control. The relations (16) do not depend on the disturbance. The relation (17) depends on the disturbance x˙ 3= x₂ sin (x₅)+x₄ cos (x₅), w, but not on the time-derivatives of the disturbance. Thus, only the estimates of the disturbances are necessary. C3YCvvu2(28) x˙ 4= −Cx₂x₆− x₄|x₄| +C+ w₂, The BDO (4) is constructed to estimate the disturbances x˙ = x, 4 4 w,i 4 i = 1, 2, 3, in (28). Note that these dis- 5 6 turbances are simulated as noisy signals and the disturbance observer estimates only their mean value.C5Nrru3 x˙ 6= −Cx₂x₄−Cx₆|x₆| +C+ w₃, However, this is fine for us, since the event-based control approach, described in Subsection 3.2, can deal6 6 6 with the noise in the disturbances. T where The situation, where the underwater vehicle starts from the point w =[w₁, w₂, w₃] represents the unknown disturbance vector. The parameter values of the model (28) (−4; 4) on a (x, x )-plane with x = 1 3 5 xare displayed in Table 4. 2= x₄ = x₆ = 0 and does circles around 0 with radius 2, is simulated. At the same time, the angle x₅ will go from 0 to the new set point The flat outputs of the system (28) are chosen as *π*/2. The parameters K, i y=i 11=, 2x,13, are all taken equal to 2. The error threshold, y₂ = x₃, and y₃ = x₅, which we also want to

is chosen as control. The relations (16) do not depend on the disturbance. The relation (17) depends on the disturbance *ε* = 0.05. Two situations are considered: first, when the disturbance estimate is continuously w,

sent to the controller. Second, when the disturbance estimate is sent to the controller only at the event times. but not on the time-derivatives of the disturbance. Thus, only the estimates of the disturbances are necessary.

The results of the case when disturbance estimate is continuously sent to the controller are displayed in The BDO (4) is constructed to estimate the disturbances wi, i = 1, 2, 3, in (28). Note that these dis-

Fig. 3. The disturbance and its estimate are presented (a) together with the output trajectories compared to

turbances are simulated as noisy signals and the disturbance observer estimates only their mean value.

their reference trajectories (b). However, this is fine for us, since the event-based control approach, described in Subsection 3.2, can deal with the noise in the disturbances. Second, the case when the disturbance estimate information is sent to the controller only on the event times, was simulated. The situation, where the underwater vehicle starts from the point The disturbance estimate is as before (Fig. 3a), however, the output trajectories are (−4; 4) on a (x₁, x₃)-plane with x₅ =

displayed in Fig. 4a. x₂ = x₄ = x₆ = 0 and does circles around 0 with radius 2, is simulated. At the same time, the angle x₅ will go from 0 to the new set point Finally, if no disturbance estimate is used in the controller design, then the corresponding output trajec- *π*/2. The parameters Ki, i = 1, 2, 3, are all taken equal to 2. The error threshold

tories are displayed in Fig.4b. The number of event times in all three cases are given in Table 5. As one can is chosen as *ε* = 0.05. Two situations are considered: 4b. first, when the disturbance estimate is continuously

expect, addition of disturbance observer reduces the number of events significantly. sent to the controller. Second, when the disturbance estimate is sent to the controller only at the event times. The results of the case when disturbance estimate is continuously sent to the controller are displayed in

Fig. 3. The disturbance and its estimate are presented (a) together with the output trajectories compared to

their reference trajectories (b).

**Table 4.** Values of the parameters for U-CAT model

Second, the case when the disturbance estimate information is sent to the controller only on the event Parameter Value Parameter Value times, was simulated. The disturbance estimate is as before (Fig. 3a), however, the output trajectories are C –40 C 59

|C1|–40|C2|59|
|---|---|---|---|
|C₃|59|C₄|40|
|C₅|–19|C₆|2.8179|
|Xuu Nrr|56 0.7226|Yvv|551|

1 2 displayed in Fig. 4a. Finally, if no disturbance estimate is used in the controller design, then the corresponding output trajec- tories are displayed in Fig.4b. The number of event times in all three cases are given in Table 5. As one can expect, addition of disturbance observer reduces the number of events significantly.

|70||||||||Proceedings of the Estonian Academy of Sciences, 2020, 69|, 1, 57–73|
|---|---|---|---|---|---|---|---|---|---|
|(a)||||||(b)||||
|(a)||(a)||||(b)|(b)|||
||1 1 ww 2 2 ww|11 00 -1 -100 22 00 -2 -200|55 10 15 20 10 15 20 55 10 15 20 10 15 20|25 25 25 25|30 30 30 30|yy yy|55 1 1 00 -5 -500 55 2 2 00 -5 -500|55 10 15 20 25 30 10 15 20 25 30 55 10 15 20 25 30 10 15 20 25 30||
|||1.5 1.5||actual actual|||33|||
|||11||estimated estimated|||2|||
|ww|3 3|0.5 0.5 00 -0.5 -0.500|55 10 15 20 10 15 20 tt|25 25|30 30|y y|3 3 12 1 00 00|reference reference actual actual 55 10 15 20 25 30 10 15 20 25 30 tt||
|Fig. 3.|Figure 3. Figure 3.||when continuous disturbance estimate signal is sent to the controller. continuous disturbance estimate signal is sent to the controller. when continuous disturbance estimate signal is sent to the controller.|||(a) The disturbance estimation results for the U-Cat model; (b) The output trajectories of the U-Cat model in the case (a) The disturbance estimation results for the UCat model; (b) The output trajectories of the UCat model in the case whe (a) The disturbance estimation results for the U-Cat model; (b) The output trajectories of the U-Cat model in the casen||||
|(a)||(a)||||(b)|(b)|||
|(a)|1 y|5 50||||(b) y|5 1 50|||
|||-5|||||-5|||
||1 y|0 0 -55|5 10 15 20|25|30|y|1 0 0 5 -5 0|5 10 15 20 25 30||
||2 y|0 50|5 10 15 20|25|30|y|2 50|5 10 15 20 25 30||
|||-5|||||-5|||
||2 y 3 y 3 y|0 0 -53 20 31 20 1 0 0|5 10 15 20 5 10 15 20 5 10 15 20 t|25 25 reference actual 25 reference actual|30 30 30|y y y|2 0 0 3 -520 3 31 20 3 1 0 0|5 10 15 20 25 30 5 10 15 20 25 30 reference actual 5 10 15 20 30 reference25 t actual||
|||0|5 10 15 20|25|30||0|5 10 15 20 25 30||
|Fig. 4.|Figure 4. Figure 4.||t Table 5.|Scenario No disturbance estimate added to the controller Constant disturbance estimate sent to the controller Disturbance estimate sent to the controller at event times|at event times; (b) The output trajectories of the U-Cat model in the case when no disturbance estimate is sent to the controller. event times; (b) The output trajectories of the UCat model in the case when no disturbance estimate is sent to the controller. at event times; (b) The output trajectories of the U-Cat model in the case when no disturbance estimate is sent to the controller.|(a) The output trajectories of the U-Cat model in the case when disturbance estimate signal is sent to the controller only (a) The output trajectories of the UCat model in the case when disturbance estimate signal is sent to the controller only a (a) The output trajectories of the U-Cat model in the case when disturbance estimate signal is sent to the controller only Number of event times in different scenarios||t Number of events 64 15 20|t|

## 5. CONCLUSIONS

A brief overview of disturbance observer approaches was given with focus on two of the most popular ones: the basic disturbance observer and the extended state observer. These methods were described in detail and compared with respect to their applicability. Then the disturbance estimates were integrated into the flatness-based control (feedback linearization based and event-based approaches) and the effectiveness of the combination was demonstrated on three practical examples: the HVAC, the AMB and the underwater vehicle models. Some future research directions for disturbance observers were mentioned in Subsection 2.5. As for the event-based control together with the integrated disturbance observer, it remains to prove the stability of the closed-loop system.

## ACKNOWLEDGEMENTS

The work of A. Kaldmae and ¨ U. Kotta were supported by the Estonian Center of Excellence in IT (EXCITE), ¨ funded by the European Regional Development Fund. The publication costs of this article were covered by the Estonian Academy of Sciences.

## REFERENCES

1. Bu, X.-W., Wu, X.-Y., Chen, Y.-X., and Bai, R.-Y. Design of a class of new nonlinear disturbance observers based on tracking differentiators for uncertain dynamic systems. Int. J. Control Autom. Syst., 2015,**13**(3), 595–602.
2. Castillo, A., Garc´ıa, P., Sanz, R., and Albertos, P. Enhanced extended state observer-based control for systems with mismatched uncertainties and disturbances. ISA Trans., 2018,**73**, 1–10.
3. Chakrabarty, A., Corless, M. J., Buzzard, G. T., Zak, S. H., and Rundell, A. E. State and unknown input observers for nonlinear systems with bounded exogenous inputs. IEEE Trans. Autom. Control, 2017,**62**(11), 5497–5510.
4.4. Chang, J.-L. Robust output feedback disturbance rejection control by simultaneously estimating state and disturbance. Chang, J.L. Robust Output Feedback Disturbance Rejection Control by Simultaneously Estimating State and Disturbance J. Control. Sci. Eng. *J*. *Control Sci*,**2011**. *Eng*, 13 pages.., 2011, **2011**, 13 pages.
5. Chang, J.-L. Applying discrete-time proportional integral observers for state and disturbance estimations. IEEE Trans. Autom. Control, 2006,**51**(5), 814–818.
6. Chaudhari, S. D., Shendge, P. D., and Phadke, S. B. Comment on ‘Comments on “A new kind of nonlinear disturbance ob- server for nonlinear systems with applications to cruise control of air-breathing hypersonic vehicles”’. Int J. Control, 2018. [https://doi.org/10.1080/00207179.2018.1559361](https://doi.org/10.1080/00207179.2018.1559361).
7. Chen, W.-H. Disturbance observer based control for nonlinear systems. IEEE/ASME Trans. Mechatron., 2004,**9**(4), 706–710.
8. Chen, W. H. Development of nonlinear disturbance observer based control and nonlinear PID: a personal note. Control Theory and Technol., 2018,**16**(4), 284–300.
9. Chen, W.-H., Ballance, D. J., Gawthrop, P. J., and O’Reilly, J. A nonlinear disturbance observer for robotic manipulators. IEEE Trans. Ind. Electron., 2000,**47**(4), 932–938.
10. Chen, W.-H., Yang, J., Guo, L., and Li, S. Disturbance-observer-based control and related methods – an overview. IEEE Trans. Ind. Electron., 2016,**63**(2), 1083–1095.
11. Chen, X., Su, C.-Y., and Fukuda, T. A nonlinear disturbance observer for multivariable systems and its application to magnetic bearing systems. IEEE Trans. Control Syst.Technol., 2004,**12**(4), 569–577.
12. Dasgupta, S., Sadhu, S., and Ghoshal, T. K. Designing disturbance observer for non-linear systems – a Hirschorn inverse approach. IET Sci., Meas. Technol., 2017,**11**(2), 164–170.
13. Do, T. D. and Nguyen, H. T. A generalized observer for estimating fast varying disturbances. IEEE Access, 2018, **6**, 28054– 28063.
14. Fliess, M., Levine, J., Martin, P., and Rouchon, P. Flatness and defect of nonlinear systems: introductory theory and examples. ´ Int. J. Control, 1995,**61**(6), 1327–1361.
15. Fliess, M., Levine, J., Martin, P., and Rouchon, P. A Lie-B ´ acklund approach to equivalence and flatness of nonlinear systems. ¨ IEEE Trans. Autom. Control, 1999,**44**(5), 922–937.
16. Ginoya, D., Shendge, P. D., and Phadke, S. B. Sliding-mode control for mismatched uncertain systems using an extended disturbance observer. IEEE Trans. Ind. Electron., 2014,**61**(4), 1983–1992.
17. Grochmal, T. R. and Lynch, A. F. Precision tracking of a rotating shaft with magnetic bearings by nonlinear decoupled disturb- ance observers. IEEE Trans. Control Syst. Technol., 2007,**15**(6), 1112–1121.

18. Guo, L. and Chen, W.-H. Disturbance attenuation and rejection for systems with nonlinearity via DOBC approach. Int. J. Robust Nonlinear Control, 2005,, 109–125.
19. Guoa, B.-Z. and Zhao, Z.-L. On the convergence of an extended state observer for nonlinear systems with uncertainty. Syst. Control Lett., 2011,**60**, 420–430.
20. Han, Y., Li, P., and Zheng, Z. A novel fixed-time sliding mode disturbance observer for a class of nonlinear systems with unmatched disturbances. In Proceedings of the 36th Chinese Control Conference. Dalian, China, 2017, 3652–3656. [https://doi.org/10.23919/ChiCC.2017.8027926](https://doi.org/10.23919/ChiCC.2017.8027926).
21. Isidori, A. Nonlinear control systems. Springer-Verlag, London, 1995.
22. Johnson, C. D. Real-time disturbance-observers; origin and evolution of the idea part 1: the early years. In Proceedings of the 40th Southeastern Symposium on System Theory. New Orleans, USA, 2008, 88–91. [https://doi.org/10.1109/SSST.2008.4480196](https://doi.org/10.1109/SSST.2008.4480196).
23. Kaldmae, A. and Kotta, ¨ U. Comments on “A new kind of nonlinear disturbance observer for nonlinear systems with applica-¨ tions to cruise control of air-breathing hypersonic vehicles”. Int. J. Control, 2018. [https://doi.org/10.1080/00207179.2018](https://doi.org/10.1080/00207179.2018). 1529436.
24. Kaldmae, A., Kotta, ¨ U., Meurer, C., and Simha, A. Event-based control for differentially flat systems: application to autonomous ¨ underwater vehicle. In Proceedings of the 11th IFAC Symposium on Nonlinear Control Systems. Vienna, Austria, 2019. [https://doi.org/10.1016/j.ifacol.2019.11.775](https://doi.org/10.1016/j.ifacol.2019.11.775).
25. Kayacan, E. and Fossen, T. I. Feedback linearization control for systems with mismatched uncertainties via disturbance ob- servers. Asian J. Control, 2019,**21**(4), 1–13.
26. Kayacan, E., Peschel, J. M., and Chowdhary, G. A self-learning disturbance observer for nonlinear systems in feedback-error learning scheme. Eng. Appl. Artif. Intell., 2017,**62**, 276–285.
27. Kim, K. S. and Rew, K. H. Reduced order disturbance observer for discrete-time linear systems. Automatica, 2013, **49**(4), 968–975.
28. Kim, K.-S., Rew, K.-H., and Kim, S. Disturbance observer for estimating higher order disturbances in time-series expansion. IEEE Trans. Autom. Control, 2010,**55**(8), 1905–1911.
29. Levine, J. ´ Analysis and Control of Nonlinear Systems: A Flatness-based Approach. Springer, Berlin, 2009.
30. Li, J.-N. and Li, L.-S. Reliable control for bilateral teleoperation systems with actuator faults using fuzzy disturbance observer. IET Control Theory Appl., 2017,**11**(3), 446–455.
31. Li, S., Yang, J., Chen, W.-H., and Chen, X. Generalized extended state observer based control for systems with mismatched uncertainties. IEEE Trans. Ind. Electron., 2012,**59**(12), 4792–4802.
32. Li, S., Yang, J., Chen, W.-H., and Chen, X. Disturbance Observer-Based Control: Methods and Applications. CRC Press, Boca Raton, 2014.
33. Liu, C., Liu, G., and Fang, J. Feedback linearization and extended state observer-based control for rotor-AMBs system with mismatched uncertainties. IEEE Trans. Ind. Electron., 2017,**64**(2), 1313–1322.
34. Lu, Y.-S. Sliding-mode disturbance observer with switching-gain adaptation and its application to optical disk drives. IEEE Trans. Ind. Electron., 2009,**56**(9), 3743–3750.
35. Ma, Y., Kelman, A., Daly, A., and Borrelli, F. Predictive control for energy efficient buildings with thermal storage: modeling, stimulation, and experiments. IEEE Control Syst. Mag., 2012,**32**(1), 44–64.
36. Maslen, E. H. Self-sensing magnetic bearings. In Magnetic Bearings: Theory, Design and Application to Rotating Machinery (Schweitzer, G. and Maslen, E. H., eds). Springer, Berlin/Heidelberg, 2013, 435–459.
37. Mohammadi, A., Marquez, H. J., and Tavakoli, M. Nonlinear disturbance observers: design and applications to Euler-Lagrange systems. IEEE Control Syst. Mag., 2017,**37**(4), 50–72.
38. Nijmeijer, H. and van der Schaft, A. Nonlinear Dynamical Control Systems. Springer-Verlag, New York, 1990.
39. Noshadi, A., Shi, J., Lee, W. S., Shi, P., and Kalam, A. Repetitive disturbance observer-based control for an active mag- netic bearing system. In Proceedings of the 5th Australian Control Conference. Gold Coast, Australia, 2015, 55–60. [https://ieeexplore.ieee.org/document/7361905](https://ieeexplore.ieee.org/document/7361905).
40. Peng, C., Fang, J., and Xu, X. Mismatched disturbance rejection control for voltage-controlled active magnetic bearing via state-space disturbance observer. IEEE Trans. Power Electron., 2015,**30**(5), 2753–2762.
41. Ran, M., Wang, Q., and Dong, C. Active disturbance rejection control for uncertain nonaffine-in-control nonlinear systems. IEEE Trans. Autom. Control, 2017,**62**(11), 5830–5836.
42. Salumae, T., Chemori, A., and Kruusmaa, M. Motion control of a hovering biomimetic four-fin underwater robot. ¨ IEEE J. Oceanic Eng., 2019,**44**(1), 54–71.
43. Sira-Ramirez, H. and Agrawal, S. K. Differentially Flat Systems. CRC Press, New York, 2004.
44. Su, J. and Chen, W.-H. Further results on “Reduced order disturbance observer for discrete-time linear systems”. Automatica, 2018,**93**, 550–553.
45. Tan, L., Jin, G., Sun, C., and Xiong, Z. High-order disturbance observer for nonlinear systems using sliding-mode tech- nology. In Proceedings of the 30th Chinese Control And Decision Conference. Shenyang, China, 2018, 1382–1386. [https://doi.org/10.1109/CCDC.2018.8407343](https://doi.org/10.1109/CCDC.2018.8407343).

46. Tang, Z., Wang, C., and Ding, Z. Unmatched disturbance rejection for AMB systems via DOBC approach. In Proceedings of the 35th Chinese Control Conference. Chengdu, China, 2016, 5931–5935. [https://doi.org/10.1109/ChiCC.2016.7554287](https://doi.org/10.1109/ChiCC.2016.7554287).
47. Wang, S., Xu, Q., Lin, R., Yang, M., Zheng, W., and Wang, Z. Feedback linearization control for electro-hydraulic servo system based on nonlinear disturbance observer. In Proceedings of the 36th Chinese Control Conference. Dalian, China, 2017, 4940–4945. [https://doi.org/10.23919/ChiCC.2017.8028135](https://doi.org/10.23919/ChiCC.2017.8028135).
48. Wang, Z., Li, S., Yang, J., and Li, Q. Current sensorless finite-time control for buck converters with time-varying disturbances. Control Eng. Pract., 2018,**77**, 127–137.
49. Wei, X. and Guo, L. Composite disturbance-observer-based control and terminal sliding mode control for non-linear systems with disturbances. Int. J. Control, 2009,**82**(6), 1082–1098.
50. Weiland, S. and Willems, J. C. Almost disturbance decoupling with internal stability. IEEE Trans. Autom. Control, 1989,**34**(3), 277–286.
51. Xu, D., Zhou, H., and Zhang, Q. Novel robust nonlinear control of magnetic bearing system based on extended state observer. In Proceedings of the 2014 International Conference on Mechatronics and Control. Jinzhou, China, 2014, 1402–1406. [https://doi.org/10.1109/ICMC.2014.7231784](https://doi.org/10.1109/ICMC.2014.7231784).
52. Yang, J., Chen, W.-H., and Li, S. Non-linear disturbance observer-based robust control for systems with mismatched disturb- ances/uncertainties. IET Control Theory Appl., 2011,**5**(18), 2053–2062.
53. Yang, J., Chen, W.-H., Li, S., and Chen, X. Static disturbance-to-output decoupling for nonlinear systems with arbitrary disturb- ance relative degree. Int. J. Robust Nonlinear Control, 2013,**23**, 562–577.
54. Yang, J., Li, S., and Yu, X. Sliding-mode control for systems with mismatched uncertainties via a disturbance observer. IEEE Trans. Ind. Electron., 2013,**60**(1), 160–169.
55. Yang, Z., Meng, B., and Sun, H. A new kind of nonlinear disturbance observer for nonlinear systems with applications to cruise control of air-breathing hypersonic vehicles. Int. J. Control, 2017,**90**(9), 1935–1950.
56. Zhan, K., Wang, Y., and Liu, L. Improved sliding-mode disturbance observer for nonlinear system. In Proceed- ings of the 10th International Conference on Modelling, Identification and Control. Guiyang, China, 2018, 1–5. [https://doi.org/10.1109/ICMIC.2018.8529954](https://doi.org/10.1109/ICMIC.2018.8529954).
## Luhi ¨ ulevaade ¨ hairingu ¨

## vaatlejatest mittelineaarsetes susteemides: ¨ rakendus lameduse omadusel pohinevale ˜ juhtimisele

## Arvo Kaldmae ja ¨ Ulle Kotta ¨

On antud luhi ¨ ulevaade populaarsetest h ¨ airingu hindamise meetoditest ja n ¨ aidatud, kuidas seda hinnangut ¨ on voimalik kasutada s ˜ usteemi lameduse omadusel p ¨ ohineva juhtimismeetodi t ˜ apsemaks muutmisel. Algul ¨ on antud uldine ¨ ulevaade h ¨ airingu hindamise deterministlikest meetoditest, seej ¨ arel on kirjeldatud l ¨ ahemalt ¨ kaht koige populaarsemat meetodit eeldusel, et leidub h ˜ airingu l ¨ oplikku j ˜ arku tuletis, mis on null. Esi-¨ mene neist on nn tavaline hairingu vaatleja. Lihtsustatult ¨ oeldes p ¨ ohineb antud vaatleja s ˜ usteemi olekute ¨ mo˜ odetud v ˜ a¨artuste ja mudeli poolt ennustatud v ¨ a¨artuste v ¨ ordlemisel. Seega eeldab antud meetod, et k ˜ oik ˜ susteemi olekud oleksid m ¨ o˜ odetavad. Teine meetod h ˜ airingu hindamiseks on nn laiendatud olekutaastaja ¨ konstrueerimine. Antud juhul laiendatakse susteemi olekuruumi h ¨ airingute ja mingi l ¨ opliku arvu h ˜ airingute ¨ tuletistega. Laiendatud susteem eeldatakse olevat h ¨ airinguvaba ja sellise laiendatud s ¨ usteemi jaoks konst-¨ rueeritakse olekutaastaja, mis muuhulgas hindab ka esialgse susteemi h ¨ airinguid ning selle tuletisi. Artiklis ¨ on pohjalikumalt v ˜ orreldud neid kaht meetodit nende rakendamise v ˜ oimalikkuse vaatepunktist. T ˜ o¨ o¨ teises pooles on naidatud, kuidas h ¨ airingute hinnanguid saab kasutada lamedate s ¨ usteemide juhtimiseks. H ¨ airingu ¨ vaatleja kombineeritakse tagasisidega lineariseerimisel pohineva juhtimismeetodi ja uudse s ˜ undmusp ¨ ohise ˜ juhtimismeetodiga, mille tulemusel saavutatakse tapsem tulemus. T ¨ o¨ o viimases osas on n ¨ aidatud kolmel ¨ praktilisel naitel (k ¨ utte- ja ventilatsioonis ¨ usteemil, aktiivsel magnetlaagers ¨ usteemil ning veealusel robotil) ¨ eelkirjeldatud hairingu hindamise kui ka t ¨ aiustatud juhtimismeetodite tulemuslikkust. ¨
