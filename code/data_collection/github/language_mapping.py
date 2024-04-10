_LANG_TO_EXTENSION = {
    "Assembly": ["asm"],
    "Batchfile": ["bat", "cmd"],
    "C": ["c", "h"],
    "C#": ["cs"],
    "C++": ["cpp", "hpp", "c++", "h++", "cc", "hh", "C", "H"],
    "CMake": ["cmake"],
    "CSS": ["css"],
    "Dockerfile": ["dockerfile", "Dockerfile"],
    "FORTRAN": ['f90', 'f', 'f03', 'f08', 'f77', 'f95', 'for', 'fpp'],
    "GO": ["go"],
    "Haskell": ["hs"],
    "HTML":["html"],
    "Java": ["java"],
    "JavaScript": ["js"],
    "Julia": ["jl"],
    "Lua": ["lua"],
    "Makefile": ["Makefile"],
    "Markdown": ["md", "markdown"],
    "PHP": ["php", "php3", "php4", "php5", "phps", "phpt"],
    "Perl": ["pl", "pm", "pod", "perl"],
    "PowerShell": ['ps1', 'psd1', 'psm1'],
    "Python": ["py"],
    "Ruby": ["rb"],
    "Rust": ["rs"],
    "SQL": ["sql"],
    "Scala": ["scala"],
    "Shell": ["sh", "bash", "command", "zsh"],
    "TypeScript": ["ts", "tsx"],
    "TeX": ["tex"],
    "Visual Basic": ["vb"]
}

_EXTENSION_TO_LANG = {}
for lang in _LANG_TO_EXTENSION:
    for extension in _LANG_TO_EXTENSION[lang]:
        _EXTENSION_TO_LANG[extension] = lang