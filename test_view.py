import re

with open('items/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'def edit_characteristics_stats\(request, character_pk\):(.*?)return render\(request, \'items/characteristics_form\.html\', context\)', re.DOTALL)

new_func = """def edit_characteristics_stats(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk)
    
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only edit your own characters.")
    
    stats, created = CharacteristicsStats.objects.get_or_create(character=character)
    
    if request.method == 'POST':
        form = CharacteristicsStatsForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            return redirect('character-profile', pk=character_pk)
    else:
        form = CharacteristicsStatsForm(instance=stats)
        
    # Group fields for rendering
    field_groups = [
        ('KELOMPOK A - CORE PVP DEFENSE (Bobot: 2.0)', [form[f'a{i}'] for i in range(1, 13)]),
        ('KELOMPOK B - CORE PVP OFFENSE (Bobot: 1.8)', [form[f'b{i}'] for i in range(1, 10)]),
        ('KELOMPOK C - CROWD CONTROL (Bobot: 1.5)', [form[f'c{i}'] for i in range(1, 18)]),
        ('KELOMPOK D - SURVIVAL (Bobot: 1.2)', [form[f'd{i}'] for i in range(1, 9)]),
        ('KELOMPOK E - SECONDARY DEFENSE (Bobot: 1.0)', [form[f'e{i}'] for i in range(1, 11)]),
        ('KELOMPOK F - SECONDARY OFFENSE (Bobot: 1.0)', [form[f'f{i}'] for i in range(1, 14)]),
    ]
        
    context = {
        'form': form,
        'field_groups': field_groups,
        'character': character,
        'title': f'Edit Characteristics for {character.name}',
        'form_description': 'Detailed breakdown of all combat statistics.'
    }
    return render(request, 'items/characteristics_form.html', context)"""

new_content, count = pattern.subn(new_func, content)
print(count)
if count > 0:
    with open('items/views.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
