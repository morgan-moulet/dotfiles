function extract --description "Universal archive extraction utility"
    if test (count $argv) -eq 0
        echo "Usage: extract <archive_file>"
        return 1
    end

    for file in $argv
        if not test -f "$file"
            echo "extract: '$file' is not a valid file"
            continue
        end

        switch $file
            case '*.tar.bz2' '*.tbz2'
                tar -xjf "$file"
            case '*.tar.gz' '*.tgz'
                tar -xzf "$file"
            case '*.tar.xz' '*.txz'
                tar -xJf "$file"
            case '*.tar.zst'
                tar --zstd -xf "$file"
            case '*.tar'
                tar -xf "$file"
            case '*.bz2'
                bunzip2 "$file"
            case '*.rar'
                unrar x "$file"
            case '*.gz'
                gunzip "$file"
            case '*.zip'
                unzip -q "$file"
            case '*.Z'
                uncompress "$file"
            case '*.7z'
                7z x "$file"
            case '*'
                echo "extract: '$file' cannot be extracted via extract"
        end
    end
end
