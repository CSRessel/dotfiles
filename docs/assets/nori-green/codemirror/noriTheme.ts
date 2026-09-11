import { EditorView } from '@codemirror/view';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { tags } from '@lezer/highlight';

const noriEditorTheme = EditorView.theme(
  {
    '&': {
      backgroundColor: '#161616',
      color: '#f2f4f8',
    },
    '.cm-content': {
      caretColor: '#6fdc8c',
    },
    '.cm-cursor, .cm-dropCursor': {
      borderLeftColor: '#6fdc8c',
    },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection':
      {
        backgroundColor: '#2a3b2e',
      },
    '.cm-panels': {
      backgroundColor: '#1c1c1c',
      color: '#f2f4f8',
    },
    '.cm-panels.cm-panels-top': {
      borderBottom: '1px solid #393939',
    },
    '.cm-panels.cm-panels-bottom': {
      borderTop: '1px solid #393939',
    },
    '.cm-searchMatch': {
      backgroundColor: '#2a3b2e',
      outline: '1px solid #42be65',
    },
    '.cm-searchMatch.cm-searchMatch-selected': {
      backgroundColor: '#42be6540',
    },
    '.cm-activeLine': {
      backgroundColor: '#1c1c1c',
    },
    '.cm-selectionMatch': {
      backgroundColor: '#2a3b2e80',
    },
    '&.cm-focused .cm-matchingBracket, &.cm-focused .cm-nonmatchingBracket': {
      outline: '1px solid #42be6580',
    },
    '.cm-gutters': {
      backgroundColor: '#161616',
      color: '#8a8f98',
      borderRight: '1px solid #262626',
    },
    '.cm-activeLineGutter': {
      backgroundColor: '#1c1c1c',
      color: '#f2f4f8',
    },
    '.cm-foldPlaceholder': {
      backgroundColor: '#262626',
      border: 'none',
      color: '#8a8f98',
    },
    '.cm-tooltip': {
      border: '1px solid #393939',
      backgroundColor: '#1c1c1c',
      color: '#f2f4f8',
    },
    '.cm-tooltip .cm-tooltip-arrow:before': {
      borderTopColor: '#393939',
      borderBottomColor: '#393939',
    },
    '.cm-tooltip .cm-tooltip-arrow:after': {
      borderTopColor: '#1c1c1c',
      borderBottomColor: '#1c1c1c',
    },
    '.cm-tooltip-autocomplete': {
      '& > ul > li[aria-selected]': {
        backgroundColor: '#2a3b2e',
        color: '#f2f4f8',
      },
    },
  },
  { dark: true },
);

const noriHighlightStyle = HighlightStyle.define([
  { tag: tags.keyword, color: '#be95ff' },
  {
    tag: [tags.name, tags.deleted, tags.character, tags.macroName],
    color: '#f2f4f8',
  },
  { tag: [tags.function(tags.variableName)], color: '#78a9ff' },
  { tag: [tags.labelName], color: '#f2f4f8' },
  {
    tag: [tags.color, tags.constant(tags.name), tags.standard(tags.name)],
    color: '#42be65',
  },
  { tag: [tags.definition(tags.name), tags.separator], color: '#f2f4f8' },
  {
    tag: [
      tags.typeName,
      tags.className,
      tags.changed,
      tags.annotation,
      tags.modifier,
      tags.self,
      tags.namespace,
    ],
    color: '#f2cc60',
  },
  {
    tag: [
      tags.operator,
      tags.operatorKeyword,
      tags.url,
      tags.escape,
      tags.regexp,
      tags.special(tags.string),
    ],
    color: '#08bdba',
  },
  { tag: [tags.meta, tags.comment], color: '#8a8f98' },
  { tag: tags.strong, fontWeight: 'bold' },
  { tag: tags.emphasis, fontStyle: 'italic' },
  { tag: tags.strikethrough, textDecoration: 'line-through' },
  { tag: tags.link, color: '#42be65', textDecoration: 'underline' },
  { tag: tags.heading, fontWeight: 'bold', color: '#78a9ff' },
  {
    tag: [tags.atom, tags.bool, tags.special(tags.variableName)],
    color: '#42be65',
  },
  {
    tag: [tags.processingInstruction, tags.string, tags.inserted],
    color: '#42be65',
  },
  { tag: tags.invalid, color: '#f47067' },
  { tag: tags.number, color: '#f2cc60' },
]);

export const noriTheme = [
  noriEditorTheme,
  syntaxHighlighting(noriHighlightStyle),
];
