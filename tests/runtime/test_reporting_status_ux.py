from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[2]

def load_module():
    p=ROOT/'scripts'/'interpret_progress_command.py'
    spec=importlib.util.spec_from_file_location('progress', p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_reporting_knowledge_has_four_surfaces():
    t=(ROOT/'knowledge'/'reporting-status-ux.md').read_text(encoding='utf-8').lower()
    for s in ['initial analysrapport','`refactoring-plan.md`','`status.md`','standardiserad stegslutrapport']:
        assert s in t

def test_short_commands_distinguish_execute_from_query():
    m=load_module()
    assert m.classify('Gör nästa steg')=='execute_next_step'
    assert m.classify('Fortsätt')=='execute_next_step'
    assert m.classify('Vad är nästa steg?')=='show_next_step'
    assert m.classify('Visa status')=='show_status'

def test_pr_continue_is_separate_intent():
    m=load_module()
    assert m.classify('Fortsätt med PR:n')=='continue_github_pr'

def test_templates_make_next_step_explicit():
    status=(ROOT/'templates'/'STATUS.template.md').read_text(encoding='utf-8')
    summary=(ROOT/'templates'/'step-summary.template.md').read_text(encoding='utf-8')
    assert 'Nästa rekommenderade steg' in status
    assert '**Nästa rekommenderade steg:**' in summary

def test_blocked_flow_does_not_skip_forward():
    t=(ROOT/'knowledge'/'reporting-status-ux.md').read_text(encoding='utf-8').lower()
    assert 'ange inte ett senare plansteg som nästa körbara steg' in t
    assert 'markera inte steget som completed' in t
