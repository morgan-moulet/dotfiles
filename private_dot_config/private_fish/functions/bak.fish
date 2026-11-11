function bak --description "Create a timestamped backup copy of a file or directory"
    if test (count $argv) -eq 0
        echo "Usage: bak <file_or_directory>"
        return 1
    end

    for target in $argv
        if not test -e "$target"
            echo "bak: '$target' does not exist"
            continue
        end

        set -l timestamp (date "+%Y%m%d_%H%M%S")
        set -l backup_name (string replace -r '/+$' '' $target)".bak_$timestamp"
        cp -a "$target" "$backup_name"
        echo "Backed up '$target' -> '$backup_name'"
    end
end
