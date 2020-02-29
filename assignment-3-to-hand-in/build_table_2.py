def basic_table():
    #from PyRTF.Elements import Document, Section, BorderPropertySet, FramePropertySet, Table
    from PyRTF.utils import RTFTestCase
    from PyRTF.Elements import Document
    from PyRTF.document.section import Section
    from PyRTF.document.paragraph import Cell, Paragraph, Table
    #from PyRTF.Styles import TextStyle, ParagraphStyle
    from PyRTF.document.character import Text
    from PyRTF.PropertySets import BorderPropertySet, FramePropertySet, MarginsPropertySet, ParagraphPropertySet, TabPropertySet, TextPropertySet
    #
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    #
    thin_edge = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.Black)
    thick_edge = BorderPropertySet(width=80, style=BorderPropertySet.SINGLE)
    zero_edge_thin = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.White)
    #
    thin_frame = FramePropertySet(thin_edge, thin_edge, thin_edge, thin_edge)
    thick_frame = FramePropertySet(thick_edge, thick_edge, thick_edge, thick_edge)
    thin_frame_top_only = FramePropertySet(top=thin_edge, left=None, bottom=None,right=None)
    thin_frame_bottom_only = FramePropertySet(top=None, left=None, bottom=thin_edge,right=None)
    thin_frame_top_and_bottom_only = FramePropertySet(top=thin_edge, left=None, bottom=thin_edge, right=None)
    #
    table = Table(TabPropertySet.DEFAULT_WIDTH * 5, TabPropertySet.DEFAULT_WIDTH * 3)
    #
    c1 = Cell(Paragraph(''), thin_frame_top_and_bottom_only)
    c2 = Cell(Paragraph('Recommends AI'), thin_frame_top_and_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph('Read ethics article'), thin_frame_top_only)
    c2 = Cell(Paragraph('-.38***'), thin_frame_top_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_top_only)
    table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph(''), thin_frame_bottom_only)
    c2 = Cell(Paragraph('(.013)'), thin_frame_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_bottom_only)
    table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph('Observations'), thin_frame_top_only)
    c2 = Cell(Paragraph('5000'), thin_frame_top_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2)
    #
    tps = TextPropertySet(italic=True)
    text = Text('R^2', tps)
    #
    #c1 = Cell(Paragraph('R^2', text), thin_frame_bottom_only)
    c1 = Cell(Paragraph(text), thin_frame_bottom_only)
    c2 = Cell(Paragraph('0.147'), thin_frame_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_bottom_only)
    table.AddRow(c1, c2)
    #
    section.append(table)
    #
    section.append('Standard errors in parentheses')
    section.append('* p<0.1, ** p<0.05, *** p<0.01')
    #
    return doc

def basic_table_with_input(dependent_variable_name, rows_statistical_significance, number_of_observations, r_squared):
    #from PyRTF.Elements import Document, Section, BorderPropertySet, FramePropertySet, Table
    from PyRTF.utils import RTFTestCase
    from PyRTF.Elements import Document
    from PyRTF.document.section import Section
    from PyRTF.document.paragraph import Cell, Paragraph, Table
    #from PyRTF.Styles import TextStyle, ParagraphStyle
    from PyRTF.document.character import Text
    from PyRTF.PropertySets import BorderPropertySet, FramePropertySet, MarginsPropertySet, ParagraphPropertySet, TabPropertySet, TextPropertySet
    #
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    #
    thin_edge = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.Black)
    thick_edge = BorderPropertySet(width=80, style=BorderPropertySet.SINGLE)
    zero_edge_thin = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.White)
    #
    thin_frame = FramePropertySet(thin_edge, thin_edge, thin_edge, thin_edge)
    thick_frame = FramePropertySet(thick_edge, thick_edge, thick_edge, thick_edge)
    thin_frame_top_only = FramePropertySet(top=thin_edge, left=None, bottom=None,right=None)
    thin_frame_bottom_only = FramePropertySet(top=None, left=None, bottom=thin_edge,right=None)
    thin_frame_top_and_bottom_only = FramePropertySet(top=thin_edge, left=None, bottom=thin_edge, right=None)
    zero_frame = FramePropertySet(top=None, left=None, bottom=None, right=None)
    #
    table = Table(TabPropertySet.DEFAULT_WIDTH * 5, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3)
    #
    c1 = Cell(Paragraph(''), thin_frame_top_and_bottom_only)
    c2 = Cell(Paragraph(dependent_variable_name + ' - coeff'), thin_frame_top_and_bottom_only)
    c3 = Cell(Paragraph(dependent_variable_name + ' - Std error'), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2, c3)
    #
    for row in rows_statistical_significance:
        c1 = Cell(Paragraph(row[0]), zero_frame)
        c2 = Cell(Paragraph(row[1]), zero_frame)
        c3 = Cell(Paragraph(row[2]), zero_frame)
        table.AddRow(c1, c2, c3)
    #
    #c1 = Cell(Paragraph(''), thin_frame_bottom_only)
    #c2 = Cell(Paragraph('(.013)'), thin_frame_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_bottom_only)
    #table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph('Observations'), thin_frame_top_only)
    c2 = Cell(Paragraph(number_of_observations), thin_frame_top_only)
    c3 = Cell(Paragraph(''), thin_frame_top_only)
    table.AddRow(c1, c2, c3)
    #
    tps = TextPropertySet(italic=True)
    text = Text('R^2', tps)
    #
    #c1 = Cell(Paragraph('R^2', text), thin_frame_bottom_only)
    c1 = Cell(Paragraph(text), thin_frame_bottom_only)
    c2 = Cell(Paragraph(r_squared), thin_frame_bottom_only)
    c3 = Cell(Paragraph(''), thin_frame_bottom_only)
    table.AddRow(c1, c2, c3)
    #
    section.append(table)
    #
    section.append('Standard errors in parentheses')
    section.append('* p<0.1, ** p<0.05, *** p<0.01')
    #
    return doc

def basic_table_two_columns(dependent_variable_name_1, dependent_variable_name_2, independent_variable_name, rows_statistical_significance_1, number_of_observations_1, r_squared_1, rows_statistical_significance_2, number_of_observations_2, r_squared_2):
    #from PyRTF.Elements import Document, Section, BorderPropertySet, FramePropertySet, Table
    from PyRTF.utils import RTFTestCase
    from PyRTF.Elements import Document
    from PyRTF.document.section import Section
    from PyRTF.document.paragraph import Cell, Paragraph, Table
    #from PyRTF.Styles import TextStyle, ParagraphStyle
    from PyRTF.document.character import Text
    from PyRTF.PropertySets import BorderPropertySet, FramePropertySet, MarginsPropertySet, ParagraphPropertySet, TabPropertySet, TextPropertySet
    #
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    #
    thin_edge = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.Black)
    thick_edge = BorderPropertySet(width=80, style=BorderPropertySet.SINGLE)
    zero_edge_thin = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.White)
    #
    thin_frame = FramePropertySet(thin_edge, thin_edge, thin_edge, thin_edge)
    thick_frame = FramePropertySet(thick_edge, thick_edge, thick_edge, thick_edge)
    thin_frame_top_only = FramePropertySet(top=thin_edge, left=None, bottom=None,right=None)
    thin_frame_bottom_only = FramePropertySet(top=None, left=None, bottom=thin_edge,right=None)
    thin_frame_top_and_bottom_only = FramePropertySet(top=thin_edge, left=None, bottom=thin_edge, right=None)
    zero_frame = FramePropertySet(top=None, left=None, bottom=None, right=None)
    #
    table = Table(TabPropertySet.DEFAULT_WIDTH * 5, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3)
    #
    c1 = Cell(Paragraph(''), thin_frame_top_and_bottom_only)
    c2 = Cell(Paragraph(dependent_variable_name_1), thin_frame_top_and_bottom_only)
    c3 = Cell(Paragraph(dependent_variable_name_2), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2, c3)
    #rows_statistical_significance_1
    c1 = Cell(Paragraph(independent_variable_name), zero_frame)
    c2 = Cell(Paragraph(rows_statistical_significance_1[0][1]), zero_frame)
    c3 = Cell(Paragraph(rows_statistical_significance_2[0][1]), zero_frame)
    table.AddRow(c1, c2, c3)
    #
    c1 = Cell(Paragraph(''), zero_frame)
    c2 = Cell(Paragraph(rows_statistical_significance_1[0][2]), zero_frame)
    c3 = Cell(Paragraph(rows_statistical_significance_2[0][2]), zero_frame)
    table.AddRow(c1, c2, c3)
    #
    #c1 = Cell(Paragraph(''), thin_frame_bottom_only)
    #c2 = Cell(Paragraph('(.013)'), thin_frame_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_bottom_only)
    #table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph('Observations'), thin_frame_top_only)
    c2 = Cell(Paragraph(number_of_observations_1), thin_frame_top_only)
    c3 = Cell(Paragraph(number_of_observations_2), thin_frame_top_only)
    table.AddRow(c1, c2, c3)
    #
    tps = TextPropertySet(italic=True)
    text = Text('R^2', tps)
    #
    #c1 = Cell(Paragraph('R^2', text), thin_frame_bottom_only)
    c1 = Cell(Paragraph(text), thin_frame_bottom_only)
    c2 = Cell(Paragraph(r_squared_1), thin_frame_bottom_only)
    c3 = Cell(Paragraph(r_squared_2), thin_frame_bottom_only)
    table.AddRow(c1, c2, c3)
    #
    section.append(table)
    #
    section.append('Standard errors in parentheses')
    section.append('* p<0.1, ** p<0.05, *** p<0.01')
    #
    return doc

def balance_table(rows, number_of_observations_1, number_of_observations_2):
    #from PyRTF.Elements import Document, Section, BorderPropertySet, FramePropertySet, Table
    from PyRTF.utils import RTFTestCase
    from PyRTF.Elements import Document
    from PyRTF.document.section import Section
    from PyRTF.document.paragraph import Cell, Paragraph, Table
    #from PyRTF.Styles import TextStyle, ParagraphStyle
    from PyRTF.document.character import Text
    from PyRTF.PropertySets import BorderPropertySet, FramePropertySet, MarginsPropertySet, ParagraphPropertySet, TabPropertySet, TextPropertySet
    #
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)
    #
    thin_edge = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.Black)
    thick_edge = BorderPropertySet(width=80, style=BorderPropertySet.SINGLE)
    zero_edge_thin = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=ss.Colours.White)
    #
    thin_frame = FramePropertySet(thin_edge, thin_edge, thin_edge, thin_edge)
    thick_frame = FramePropertySet(thick_edge, thick_edge, thick_edge, thick_edge)
    thin_frame_top_only = FramePropertySet(top=thin_edge, left=None, bottom=None,right=None)
    thin_frame_bottom_only = FramePropertySet(top=None, left=None, bottom=thin_edge,right=None)
    thin_frame_top_and_bottom_only = FramePropertySet(top=thin_edge, left=None, bottom=thin_edge, right=None)
    zero_frame = FramePropertySet(top=None, left=None, bottom=None, right=None)
    #
    table = Table(TabPropertySet.DEFAULT_WIDTH * 5, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3)
    #
    c1 = Cell(Paragraph(''), thin_frame_top_and_bottom_only)
    c2 = Cell(Paragraph('Control'), thin_frame_top_and_bottom_only)
    c3 = Cell(Paragraph('Treatment'), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2, c3)
    #rows_statistical_significance_1
    c1 = Cell(Paragraph(rows[0][0]), zero_frame)
    c2 = Cell(Paragraph(rows[0][1]), zero_frame)
    c3 = Cell(Paragraph(rows[0][2]), zero_frame)
    table.AddRow(c1, c2, c3)
    #
    c1 = Cell(Paragraph(rows[1][0]), zero_frame)
    c2 = Cell(Paragraph(rows[1][1]), zero_frame)
    c3 = Cell(Paragraph(rows[1][2]), zero_frame)
    table.AddRow(c1, c2, c3)
    #
    c1 = Cell(Paragraph(rows[2][0]), zero_frame)
    c2 = Cell(Paragraph(rows[2][1]), zero_frame)
    c3 = Cell(Paragraph(rows[2][2]), zero_frame)
    table.AddRow(c1, c2, c3)
    #
    #c1 = Cell(Paragraph(''), thin_frame_bottom_only)
    #c2 = Cell(Paragraph('(.013)'), thin_frame_bottom_only)
    #c3 = Cell(Paragraph('tbd'), thin_frame_bottom_only)
    #table.AddRow(c1, c2)
    #
    c1 = Cell(Paragraph('Observations'), thin_frame_top_and_bottom_only)
    c2 = Cell(Paragraph(number_of_observations_1), thin_frame_top_and_bottom_only)
    c3 = Cell(Paragraph(number_of_observations_2), thin_frame_top_and_bottom_only)
    table.AddRow(c1, c2, c3)
    #
    section.append(table)
    #
    return doc
