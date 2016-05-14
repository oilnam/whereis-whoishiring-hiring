import sys
from full_hn_reindex import process_page

def main():
    if len(sys.argv) != 2:
        print('usage: python {0} <hn_post_id>'.format(sys.argv[0]))
        sys.exit(1)

    # update is set to True when we want to delete the jobs before
    # reindexing the given month
    process_page(sys.argv[1], update = True)


if __name__== "__main__":
    main()

