function cheat --description "Query cheat.sh community cheatsheets for any command"
    if test (count $argv) -eq 0
        echo "Usage: cheat <command_or_topic> (e.g. 'cheat tar', 'cheat rsync', 'cheat docker')"
        return 1
    end

    set -l query (string join '+' $argv)
    curl -m 10 -s "https://cheat.sh/$query"
end
