Doctor
|----- Name
|----- Avatar
|----- Phone
( spec_id => Specialization (id) )

Specialization
|------ Name

Patient
|----- Name
|----- Avatar
|----- Age

Period
|---- period_id
( session_id => Session (id) )

Session
( patient_id => Patient (id) )
( doctor_id => Doctor (id) )

<!-- prettier-ignore -->
select sessions.*, doctors.name as dname, doctors.avatar as davatar, doctors.phone as dphone, patients.name as pname, patients.avatar as pavatar from sessions join doctors on sessions.doctor_id = doctors.id join patients on patients.id = sessions.patient_id join specializations on specializations.id = doctors.spec_id where patients.id = 2;

<!-- prettier-ignore -->
select sessions.*, doctors.name as dname, doctors.avatar as davatar, doctors.phone as dphone from sessions join doctors on sessions.doctor_id = doctors.id join specializations on specializations.id = doctors.spec_id where sessions.patient_id = 2;
