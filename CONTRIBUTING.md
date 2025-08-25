## Configuration and Customization

Most of the modules in this project are designed to be **modular and easily configurable**.

### Key point:

- **To modify behavior or adjust parameters, edit the `__init__` method of the corresponding class.**

Inside `__init__`, you will find parameters such as:

- Columns to read or rename
- Starting rows and indices
- Data types and cleaning rules
- Threshold values or constants

Changing these parameters customizes how the module processes data without modifying the core logic.

---

For example, in `AbsenceController`, you can change:

```python
self.StartRowAt = 7
self.pickColumns = [0,1,2,34,35,36,37]
self.rename_columns = { ... }
```
