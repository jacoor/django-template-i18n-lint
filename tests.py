"""
Unittests for django-template-i18n-lint.
"""
import unittest
import django_angular_template_i18n_lint


def _known_good_output(input_string, expected_output):
    def test(self):
        actual_output = list(django_angular_template_i18n_lint.non_translated_text(input_string))
        self.assertEqual(actual_output, expected_output)
    test.__doc__ = "Input string {0} should give output of {1}".format(
        repr(input_string[:30]), repr(expected_output)[:30])
    return test


class DjangoTemplateI18nLintTestCase(unittest.TestCase):
    """
    Unittests.
    """

    testSimple = _known_good_output("<h1>Foo</h1>", [(1, 5, 'Foo')])
    testMultiWord = _known_good_output("<h1>Foo</h1><p>Bar</p>", [(1, 5, 'Foo'), (1, 16, 'Bar')])
    testMultiWordMultiLine = _known_good_output("<h1>Foo</h1>\n<p>Bar</p>", [(1, 5, 'Foo'), (2, 4, 'Bar')])

    # Test things that shouldn't be included
    testTransOK = _known_good_output("<b>{% trans 'Foo' %}</b>", [])
    testBlocktransOK1 = _known_good_output("<b>{% blocktrans %}Foo{% endblocktrans %}</b>", [])
    testBlocktransOK2 = _known_good_output("<b>{% blocktrans with var=bar %}Foo{% endblocktrans %}</b>", [])
    testBlocktransOK3 = _known_good_output("<b>{% blocktrans with var as bar %}Foo{% endblocktrans %}</b>", [])
    testDjangoCustomTag = _known_good_output("{% load foo %}", [])
    testJS = _known_good_output("Foo<script>alert('Foo');</script>Bar", [(1, 1, 'Foo'), (1, 34, 'Bar')])
    testDjangoVar = _known_good_output("Foo{{ bar }}Baz", [(1, 1, 'Foo'), (1, 13, 'Baz')])
    testBooleanValuesOK1 = _known_good_output("<option selected>Option</option>", [(1, 18, 'Option')])
    testBooleanValuesOK2 = _known_good_output("<img src='my.jpg' ismap />", [])

    testNoHTMLAttrSingleQuote = _known_good_output("<form method='POST'>FOO</form>", [(1, 21, 'FOO')])
    testNoHTMLAttrDoubleQuote = _known_good_output("<form method=\"POST\">FOO</form>", [(1, 21, 'FOO')])
    testNoHTMLAttrNoQuote1 = _known_good_output("<form method=POST>FOO</form>", [(1, 19, 'FOO')])
    testNoHTMLAttrNoQuote2 = _known_good_output("<form method=post>FOO</form>", [(1, 19, 'FOO')])

    testNumbers = _known_good_output("<b>123.456,789</b>", [])

    testDjangoTagInAttr = _known_good_output("<img alt='{{ 'url' }}'>", [])
    testDjangoTagInAttr2 = _known_good_output('<img alt="{% "url" %}">', [])

    testNotrans1 = _known_good_output("Foo {# notrans #}", [])
    testNotrans2 = _known_good_output('{% block %}\nFoo {# notrans #}\n{% endblock %}">', [])
    testNotrans1 = _known_good_output("Foo <!-- notrans -->", [])
    testNotrans2 = _known_good_output('{% block %}\nFoo <!-- notrans -->\n{% endblock %}">', [])

    testIssue17a = _known_good_output("<input type=\"submit\" value=\"Confirm\" class=\"btn btn-danger\" />", [(1, 29, 'Confirm')])
    testIssue17b = _known_good_output('<li><a href="https://twitter.com/localunews" class="icon-twitter" rel="tooltip" title="" data-placement="top" data-original-title="Twitter"><i class="fa fa-twitter"></i></a></li>', [(1, 132, 'Twitter')])
    testIssue17c = _known_good_output('<form name="form" novalidate data-ng-submit="update(goal)">', [])
    testIssue17d = _known_good_output(
        """
        <input placeholder="{[{ 'Start Date'|translate }]}" type="text" data-field="date" data-ng-model="goal.start"
        required data-nm-date-time-picker>
        """, [])

    testAngularTemplate = _known_good_output('Foo [[yoyo]] bar', [(1, 1, 'Foo'), (1, 14, 'bar')])

    testAlt1 = _known_good_output("<img src=foo.jpg alt='Photo'>", [(1, 23, 'Photo')])
    testAlt2 = _known_good_output("<img src=foo.jpg alt=\"Photo\">", [(1, 23, 'Photo')])
    testAlt3 = _known_good_output("<img src=foo.jpg alt='{% get_title %}'>", [])
    testAlt4 = _known_good_output('<img src="foo.jpg" alt="Photo">', [(1, 25, 'Photo')])
    testAlt5 = _known_good_output('<img src=\'foo.jpg\' alt="Photo">', [(1, 25, 'Photo')])
    testAlt6 = _known_good_output("<img src=foo.jpg alt=Photo>", [(1, 22, 'Photo')])
    testAlt7 = _known_good_output("<img alt=Photo>", [(1, 10, 'Photo')])

    # arabella added tests
    testAngularTranslations1 = _known_good_output("{[{ 'some text'|translate }]}", [])
    testAngularTranslations2 = _known_good_output("{[{'some text'|translate}]}", [])
    testAngularTranslations3 = _known_good_output("{[{'some text' | translate}]}", [])
    testAngularTranslations4 = _known_good_output("<div translate>SomeText</div>", [])
    testAngularTranslations5 = _known_good_output("<div>SomeText</div>", [(1, 6, 'SomeText')])
    testAngularTranslations6 = _known_good_output("<div translate><span></span><i class='x'></i>SomeText</div>",
                                                  [(1, 46, 'SomeText')])
    testAngularTranslations7 = _known_good_output(
        "<div><span></span><i class='x'></i>{[{ 'SomeText'|translate}]}</div>", [])

    testAngularTranslations8 = _known_good_output("""
            <p class="notify_msg full" ng-if="::showSessionFullCopy" translate>
                Session Full
            </p>
        """, [])

    testArabellaDirective1 = _known_good_output("<div aa-collapsable>SomeText</div>", [(1, 21, 'SomeText')])
    testArabellaDirective2 = _known_good_output("""
        <aa-input aa-errors="errors" aa-input-model="user.height_in" aa-input-name="height_in" aa-input-field="accountFormFields.height_in" aa-extratext='in' aa-li-extra-class="columns small-6" aa-fieldwrap="extra_fieldwrap"></aa-input>
        """, [])

    testDataAttribute1 = _known_good_output('<data-aa-collapsable title="{% trans "Your Account" %}" expanded="true">',
                                            [])

if __name__ == '__main__':
    unittest.main()
