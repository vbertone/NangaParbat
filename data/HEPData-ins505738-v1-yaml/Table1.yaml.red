dependent_variables:
- header:
  qualifiers:
  - {name: process, value: DY}
  - {name: observable, value: d(sigma)/dydQdqT}
  - {name: target_isoscalarity, value: -1 }
  - {name: Vs, value: 1800}
  - {name: Q, low: 66, high: 116, integrate: true}
  - {name: y, low: -2.75, high: 2.75, integrate: true}
  values:
  - errors:
    - {label: 'unc', value: 1.2}
    - {label: 'mult', value: 0.039}
    value: 14.8
  - errors:
    - {label: 'unc', value: 1.4}
    - {label: 'mult', value: 0.039}
    value: 19.4
  - errors:
    - {label: 'unc', value: 1.4}
    - {label: 'mult', value: 0.039}
    value: 20.2
  - errors:
    - {label: 'unc', value: 1.5}
    - {label: 'mult', value: 0.039}
    value: 23.6
  - errors:
    - {label: 'unc', value: 1.4}
    - {label: 'mult', value: 0.039}
    value: 23.6
  - errors:
    - {label: 'unc', value: 1.4}
    - {label: 'mult', value: 0.039}
    value: 23.0
  - errors:
    - {label: 'unc', value: 1.3}
    - {label: 'mult', value: 0.039}
    value: 19.9
independent_variables:
- header:
  values:
  - {high: 1.5, low: 1.0}
  - {high: 2.0, low: 1.5}
  - {high: 2.5, low: 2.0}
  - {high: 3.0, low: 2.5}
  - {high: 3.5, low: 3.0}
  - {high: 4.0, low: 3.5}
  - {high: 4.5, low: 4.0}
