while getopts "" opt; do
  case $opt in
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

