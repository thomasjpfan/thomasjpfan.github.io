"""
Pelican Math Markdown Extension
"""

import markdown
from markdown.util import etree
from markdown.util import AtomicString


class PelicanKatexPattern(markdown.inlinepatterns.Pattern):
    """Inline markdown processing that matches katex"""

    def __init__(self, pelican_katex_extension, tag, pattern):
        super(PelicanKatexPattern, self).__init__(pattern)
        self.math_tag_class = pelican_katex_extension.getConfig(
            'math_tag_class'
        )
        self.pelican_katex_extension = pelican_katex_extension
        self.tag = tag

    def handleMatch(self, m):
        node = markdown.util.etree.Element(self.tag)
        node.set('class', self.math_tag_class)

        prefix = '\\(' if m.group('prefix') == '$' else m.group('prefix')
        suffix = '\\)' if m.group('suffix') == '$' else m.group('suffix')
        node.text = markdown.util.AtomicString(
            prefix + m.group('math') + suffix)

        self.pelican_katex_extension.katex_needed = True
        return node


class PelicanKatexCorrectDisplayMath(markdown.treeprocessors.Treeprocessor):
    """Corrects invalid html that results from a <div> being put
    inside a <p> for displayed math"""

    def __init__(self, pelican_katex_extension):
        self.pelican_katex_extension = pelican_katex_extension

    def correct_html(self, root, children,
                     div_math, insert_idx, text):
        """Separates out <div class="math"> from the parent tag<p>.
        Anything inbetween is put into its own parent tag of <p>"""

        current_idx = 0

        for idx in div_math:
            el = markdown.util.etree.Element('p')
            el.text = text
            el.extend(children[current_idx:idx])

            if len(el) != 0 or (el.text and not el.text.isspace()):
                root.insert(insert_idx, el)
                insert_idx += 1

            text = children[idx].tail
            children[idx].tail = None
            root.insert(insert_idx, children[idx])
            insert_idx += 1
            current_idx = idx + 1

        el = markdown.util.etree.Element('p')
        el.text = text
        el.extend(children[current_idx:])

        if len(el) != 0 or (el.text and not el.text.isspace()):
            root.insert(insert_idx, el)

    def run(self, root):
        """Searches for <div class="math"> that are children in
        <p> tags and corrects the invalid HTML that results
        """

        math_tag_class = self.pelican_katex_extension.getConfig(
            'math_tag_class'
        )

        for parent in root:
            div_math = []
            children = list(parent)

            for div in parent.findall('div'):
                if div.get('class') == math_tag_class:
                    div_math.append(children.index(div))

            if not div_math:
                continue

            insert_idx = list(root).index(parent)
            self.correct_html(root, children, div_math, insert_idx,
                              parent.text)
            root.remove(parent)

        return root


class PelicanKatexAddJavaScript(markdown.treeprocessors.Treeprocessor):
    """Tree Processor for adding Katex Javascript to blog"""

    def __init__(self, pelican_katex_extension):
        self.pelican_katex_extension = pelican_katex_extension

    def run(self, root):
        if (not self.pelican_katex_extension.katex_needed):
            return root

        katex_script = etree.Element('script')
        katex_script.set('type', 'text/javascript')
        katex_script.text = AtomicString(
            self.pelican_katex_extension.getConfig('katex_script')
        )
        root.append(katex_script)

        self.pelican_katex_extension.katex_needed = False
        return root


class PelicanKatexExtension(markdown.Extension):
    """A markdown extension enabling katex processing in Markdown
    for pelican"""

    def __init__(self, config):
        self.config['katex_script'] = ['', 'Katex Javascript script']
        self.config['math_tag_class'] = ['math',
                                         'The class of the tag in which mathematics is wrapped']
        self.config['auto_insert'] = [True,
                                      'Determines if katex script is automatically inserted']
        super().__init__(**config)

        self.katex_needed = False

    def extendMarkdown(self, md, md_globals):
        katex_inline_regex = r'(?P<prefix>\$)(?P<math>.+?)(?P<suffix>(?<!\s)\2)'
        katex_display_regex = r'(?P<prefix>\$\$|\\begin\{(.+?)\})(?P<math>.+?)(?P<suffix>\2|\\end\{\3\})'

        md.inlinePatterns.add(
            'katex_dispayed',
            PelicanKatexPattern(
                self, 'div', katex_display_regex),
            '<escape')

        md.inlinePatterns.add(
            'katex_inlined',
            PelicanKatexPattern(
                self, 'span', katex_inline_regex
            ),
            '<escape')

        md.treeprocessors.add(
            'katex_correctdisplaymath',
            PelicanKatexCorrectDisplayMath(self),
            '>inline')

        if self.getConfig('auto_insert'):
            md.treeprocessors.add(
                'katex_addjavascript',
                PelicanKatexAddJavaScript(self), '_end')
