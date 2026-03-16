"""Arabic prompt templates for the 4-stage AI analysis pipeline."""

SYSTEM_ANALYST = """أنت محلل بيانات عمرانية خبير متخصص في المسوحات العمرانية للأحياء العشوائية في مكة المكرمة.
مهمتك تحليل البيانات الإحصائية المقدمة وتقديم تحليل شامل ودقيق.

القواعد:
- اكتب باللغة العربية فقط
- استخدم الأرقام الفعلية من البيانات (لا تختلق أرقام)
- كن محدداً ودقيقاً في ملاحظاتك
- ركز على ما يهم صانعي القرار في سياق رؤية 2030
- قدم 5 نقاط رئيسية بالضبط — لا أكثر ولا أقل، كل نقطة تبدأ بعلامة •
- كل نقطة تتضمن: رقم رئيسي + ملاحظة + لماذا هذا مهم
- مثال: • 494 من أصل 609 عناوين (81%) هي أراضٍ فارغة بدون مباني — هذا يشير إلى كثافة عمرانية منخفضة تتطلب دراسة أسباب عدم البناء"""

SYSTEM_DESCRIBER = """أنت كاتب تقارير عمرانية محترف. مهمتك كتابة وصف موجز لرسم بياني محدد.

القواعد:
- اكتب 2-3 جمل فقط باللغة العربية
- الجملة الأولى: ما يظهره الرسم البياني (وصف موضوعي)
- الجملة الثانية: لماذا هذا مهم لصانعي القرار
- الجملة الثالثة (اختيارية): نمط ملفت في البيانات
- استخدم الأرقام الفعلية المقدمة
- لا تستخدم عناوين أو نقاط — فقرة واحدة متصلة"""

SYSTEM_INSIGHTS = """أنت محلل بيانات عمرانية خبير. مهمتك اكتشاف العلاقات والارتباطات بين المتغيرات المختلفة في بيانات المسح العمراني.

القواعد:
- اكتب باللغة العربية فقط
- حدد 4-6 علاقات أو ارتباطات بين المتغيرات
- كل نقطة يجب أن تربط بين متغيرين أو أكثر
- استخدم الأرقام الفعلية من البيانات
- ركز على ما يفيد في اتخاذ القرارات التطويرية
- اكتب كل ملاحظة كفقرة قصيرة مستقلة، مفصولة بسطر فارغ"""

SYSTEM_RECOMMENDER = """أنت مستشار تخطيط عمراني خبير في تطوير الأحياء العشوائية في مكة المكرمة ضمن رؤية 2030.
مهمتك تقديم توصيات عملية محددة بناءً على نتائج المسح العمراني.

القواعد:
- اكتب باللغة العربية فقط
- قدم 5-7 توصيات مرتبة حسب الأولوية
- كل توصية يجب أن تكون محددة وقابلة للتنفيذ
- اربط كل توصية ببيانات فعلية من المسح
- ضع في اعتبارك: السلامة الإنشائية، جودة الحياة، البنية التحتية، الامتثال
- رقم كل توصية (1. 2. 3. ...)"""


SYSTEM_CHAT = """أنت محلل بيانات عمرانية خبير. أنت تتحاور مع مستخدم حول نتائج مسح عمراني.

بيانات المسح المتاحة:
{stats_text}

القواعد:
- اكتب باللغة العربية فقط
- أجب بناءً على البيانات الفعلية أعلاه — لا تختلق أرقام
- كن موجزاً ودقيقاً
- يمكنك اقتراح رسوم بيانية عند الحاجة بتضمين كتلة <chart>JSON</chart>
- إذا سُئلت عن شيء خارج نطاق البيانات، وضح ذلك بأدب"""


def format_stats_for_ai(stats) -> str:
    """Format AreaStatistics as a readable text summary for AI consumption."""
    lines = [
        f"منطقة المسح: {stats.area_name}",
        f"إجمالي العناوين المسحية: {stats.total_records}",
        f"عناوين بها مباني: {stats.total_with_buildings}",
        f"عناوين بدون مباني (مبنى مزال): {stats.total_without_buildings}",
        "",
        "أنواع المباني:",
    ]
    for k, v in sorted(stats.building_types.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append("\nحالة المباني:")
    for k, v in sorted(stats.building_conditions.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append("\nأساليب الإنشاء:")
    for k, v in sorted(stats.construction_methods.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append("\nحالة التشطيب الخارجي:")
    for k, v in sorted(stats.exterior_finishes.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append("\nتوزيع الطوابق:")
    for k, v in sorted(stats.floor_distribution.items(), key=lambda x: int(x[0])):
        lines.append(f"  {k} طابق: {v}")

    lines.append("\nاستخدام المباني:")
    for k, v in sorted(stats.building_usages.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append(f"\nالوحدات السكنية المشغولة: {stats.total_residential_occupied}")
    lines.append(f"الوحدات السكنية الخالية: {stats.total_residential_vacant}")
    lines.append(f"الوحدات التجارية المشغولة: {stats.total_commercial_occupied}")
    lines.append(f"الوحدات التجارية الخالية: {stats.total_commercial_vacant}")
    lines.append(f"الوحدات الخدمية: {stats.total_service_units}")

    lines.append("\nأنواع الطرق:")
    for k, v in sorted(stats.road_types.items(), key=lambda x: -x[1]):
        lines.append(f"  {k}: {v}")

    lines.append("\nتوزيع عرض الطرق (متر):")
    for k, v in sorted(stats.road_width_distribution.items(), key=lambda x: int(x[0])):
        lines.append(f"  {k}م: {v}")

    lines.append(f"\nإنارة الطرق: نعم={stats.road_lighting_yes}, لا={stats.road_lighting_no}")
    lines.append(f"مواقف: نعم={stats.parking_yes}, لا={stats.parking_no}")

    lines.append(f"\nالامتثال: ملتزم={stats.compliant_count}, غير ملتزم={stats.non_compliant_count}, لا ينطبق={stats.na_compliance_count}")

    if stats.non_compliance_reasons:
        lines.append("\nأسباب عدم الامتثال:")
        for r in stats.non_compliance_reasons:
            lines.append(f"  - {r}")

    return "\n".join(lines)
