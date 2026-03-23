/*  rules.pl (Final Improved Version)
    Diagnostic Expert System Rule Base
*/

:- dynamic symptom/2.

/* ------------------------------------------------------------------
   DIAGNOSIS RULES
------------------------------------------------------------------ */

% 🔴 Severe infection: high fever + long duration
diagnosis(severe_infection) :-
    symptom(patient, fever_high),
    symptom(patient, duration_long).

% 🟠 Acute infection: high fever + short duration
diagnosis(acute_infection) :-
    symptom(patient, fever_high),
    symptom(patient, duration_short).

% 🟡 Mild viral fever: low fever + short duration
diagnosis(mild_viral_fever) :-
    symptom(patient, fever_low),
    symptom(patient, duration_short).

% 🟡 Prolonged fever: low fever + long duration
diagnosis(prolonged_fever) :-
    symptom(patient, fever_low),
    symptom(patient, duration_long).

% 🔵 Hypothermia: very low temperature
diagnosis(hypothermia) :-
    symptom(patient, temp_very_low).

% 🟢 Healthy condition (NEW 🔥)
diagnosis(healthy) :-
    symptom(patient, normal_temp).

% ⚪ No matching condition
diagnosis(no_clear_diagnosis) :-
    \+ symptom(patient, fever_high),
    \+ symptom(patient, fever_low),
    \+ symptom(patient, temp_very_low),
    \+ symptom(patient, normal_temp).


/* ------------------------------------------------------------------
   TREATMENT RULES
------------------------------------------------------------------ */

treatment(severe_infection,
  'High risk: seek immediate medical attention. Visit a hospital urgently and avoid self-medication.'
).

treatment(acute_infection,
  'Moderate risk: take rest, stay hydrated, and monitor temperature regularly. Consult a doctor if symptoms persist.'
).

treatment(mild_viral_fever,
  'Low risk: rest, drink fluids, and take mild medication if prescribed. Monitor symptoms.'
).

treatment(prolonged_fever,
  'Persistent fever: consult a doctor and consider diagnostic tests such as blood tests.'
).

treatment(hypothermia,
  'Dangerously low body temperature: keep warm immediately using blankets and warm fluids, and seek urgent medical help.'
).

treatment(healthy,
  'Normal condition: no fever detected. Maintain a healthy lifestyle and monitor for any symptoms.'
).

treatment(no_clear_diagnosis,
  'No clear diagnosis. Recheck inputs and consult a healthcare professional if necessary.'
).


/* ------------------------------------------------------------------
   MAIN QUERY
------------------------------------------------------------------ */

get_diagnosis(Diagnosis, TreatmentText) :-
    diagnosis(Diagnosis),
    treatment(Diagnosis, TreatmentText).