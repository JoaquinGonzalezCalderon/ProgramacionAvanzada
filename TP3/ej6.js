function isBalanced(s) {
    const open = new Set(['(', '[', '{']);
    const match = { ')': '(', ']': '[', '}': '{' };
    const stack = [];
    for (const ch of s ?? '') {
        if (open.has(ch)) {
            stack.push(ch);
        } else if (ch in match) {
            if (stack.pop() !== match[ch]) return false;
        }
    }
    return stack.length === 0;
}