# Aspect Ratio Calculation: Width for 600px Height at 16:9

## Screen reference
- Monitor resolution: **1920 × 1080**
- Aspect ratio: **1920 : 1080 = 16 : 9**

## Calculation

To find the width that preserves the 16:9 ratio at a height of 600 px:

```
width / height = 16 / 9
width = height × (16 / 9)
width = 600 × (16 / 9)
width = 600 × 1.7̄  (1.7 recurring)
width = 1066.6̄  (1066.6 recurring)
width ≈ 1067  (rounded to nearest whole pixel)
```

## Result

| Setting | Value |
|---------|-------|
| WIDTH   | 1067  |
| HEIGHT  | 600   |

## Usage in `src/settings.py`

```python
WIDTH, HEIGHT = 1067, 600
```
