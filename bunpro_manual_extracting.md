# Bunrpo manual words extracting
Since bunpro lacks official API and returns html pages for request,
here is an instruction for manual export of known words.

For example on N5 vocab deck:
1. Open empty text file
2. Open https://bunpro.jp/decks/resqiy/Bunpro-N5-Vocab
3. Open browser console by F12
4. Paste the code and press Enter
5. Switch to the text file and press Ctl+V, it should paste the word list
6. Repeat for each page in the deck
7. If needed, repeat for decks N4-N1

```javascript
copy([...document.querySelectorAll('.js_decks-card_info')].map((node)=>{
    if (node.querySelectorAll('.streak').length) {
        const textNode = node.querySelector('.deck-card-title')
        if (textNode.innerHTML.includes('ruby')) {
            return textNode.children[0].innerHTML.replace(/<rp.+/, '').trim()
        }
        return textNode.innerText.replaceAll(/（.+）/g, '')
    }
    return ''
}).filter(Boolean))
```

## Caveats

1. Script works for Chrome and Firefox. Firefox shows furigana in ruby tags, hence the branching.
2. Sometimes Bunpro opens multiple tabs when clicking on a deck, looks like some bug.