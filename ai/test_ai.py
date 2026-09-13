from ai_module import analyze_fashion

result = analyze_fashion("test_image.png")

print("\n========== AI RESULT ==========\n")

if "error" in result:
    print(result["error"])
else:
    print("1. Recommended Dress:")
    print(result["recommendation"])