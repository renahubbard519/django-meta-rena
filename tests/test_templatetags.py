from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from meta.templatetags.meta import (
    og_prop, meta, meta_list, twitter_prop, generic_prop,
    googleplus_prop, googleplus_html_scope, custom_meta, custom_meta_extras, meta_extras)


class OgPropTestCase(unittest.TestCase):
    def test_og_prop_basically_works(self):
        self.assertEqual(
            og_prop('type', 'website'),
            '<meta property="og:type" content="website">'
        )

    def test_generic_prop_basically_works(self):
        self.assertEqual(
            generic_prop('og', 'type', 'website'),
            '<meta property="og:type" content="website">'
        )

    def test_generic_prop_escapes_xss(self):
        self.assertEqual(
            generic_prop('og', 't"y&p<e', 'web&site'),
            '<meta property="og:t&quot;y&amp;p&lt;e" content="web&amp;site">'
        )


class MetaTestCase(unittest.TestCase):
    def test_meta_basically_works(self):
        self.assertEqual(
            meta('description', 'Awesome website about ponies'),
            '<meta name="description" content="Awesome website about ponies">'
        )

    def test_meta_escapes_xss(self):
        self.assertEqual(
            meta('desc"rip&tion', 'Awesome website < about ponies'),
            '<meta name="desc&quot;rip&amp;tion" content="Awesome website &lt; about ponies">'
        )


class CustomMetaTestCase(unittest.TestCase):
    def test_custom_meta_basically_works(self):
        self.assertEqual(
            custom_meta('property', 'foo', 'bar'),
            '<meta property="foo" content="bar">'
        )

    def test_custom_meta_escapes_xss(self):
        self.assertEqual(
            custom_meta('prop&erty', 'fo"o', 'b<ar'),
            '<meta prop&amp;erty="fo&quot;o" content="b&lt;ar">'
        )


class TwitterPropTestCase(unittest.TestCase):
    def test_twitter_basically_works(self):
        self.assertEqual(
            twitter_prop('foo', 'bar'),
            '<meta name="twitter:foo" content="bar">'
        )

    def test_twitter_escapes_xss(self):
        self.assertEqual(
            twitter_prop('fo"o', 'b<ar'),
            '<meta name="twitter:fo&quot;o" content="b&lt;ar">'
        )


class GooglePlusPropTestcase(unittest.TestCase):
    def test_google_plus_basically_works(self):
        self.assertEqual(
            googleplus_prop('foo', 'bar'),
            '<meta itemprop="foo" content="bar">'
        )

    def test_google_plus_scope_works(self):
        self.assertEqual(
            googleplus_html_scope('bar'),
            ' itemscope itemtype="http://schema.org/bar" '
        )

    def test_google_plus_escapes_xss(self):
        self.assertEqual(
            googleplus_prop('fo"o', 'b<ar'),
            '<meta itemprop="fo&quot;o" content="b&lt;ar">'
        )


class MetaListTestCase(unittest.TestCase):
    def test_meta_list_basically_works(self):
        self.assertEqual(
            meta_list('keywords', ['foo', 'bar', 'baz']),
            '<meta name="keywords" content="foo, bar, baz">'
        )

    def test_meta_list_with_non_list_value(self):
        self.assertEqual(
            meta_list('keywords', 12),
            ''
        )

    def test_meta_list_escapes_xss(self):
        self.assertEqual(
            meta_list('keywords', ['fo"o', 'bar', 'b<az']),
            '<meta name="keywords" content="fo&quot;o, bar, b&lt;az">'
        )


class MetaExtrasTestCase(unittest.TestCase):
    def test_meta_extras_basically_works(self):
        result = meta_extras({
            'type': 'foo',
            'image_width': 'bar'
        })
        self.assertTrue('<meta name="type" content="foo">' in result)
        self.assertTrue('<meta name="image_width" content="bar">' in result)


class CustomMetaExtrasTestCase(unittest.TestCase):
    def test_custom_meta_extras_basically_works(self):
        result = custom_meta_extras([
                ('property', 'type', 'foo'),
                ('key', 'image_width', 'bar')
        ])
        self.assertTrue('<meta property="type" content="foo">' in result)
        self.assertTrue('<meta key="image_width" content="bar">' in result)
