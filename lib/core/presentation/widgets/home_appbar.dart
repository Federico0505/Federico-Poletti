import 'package:flutter/material.dart';
import 'package:opennutritracker/core/utils/navigation_options.dart';
import 'package:opennutritracker/generated/l10n.dart';

class HomeAppbar extends StatelessWidget implements PreferredSizeWidget {
  const HomeAppbar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Row(
        children: [
          SizedBox(
            width: 40,
            child: Image.asset('assets/icon/ont_logo_square.png'),
          ),
          Row(
            children: [
              Text(S.of(context).appTitle,
                  style: TextStyle(
                      fontWeight: FontWeight.w700,
                      color: Theme.of(context).colorScheme.onBackground)),
              const SizedBox(width: 5),
              Text(
                S.of(context).alphaVersionName,
                style: TextStyle(
                    fontWeight: FontWeight.w500,
                    color: Theme.of(context).colorScheme.onBackground),
              ),
            ],
          )
        ],
      ),
      actions: [
        IconButton(
          icon: Icon(Icons.settings_outlined,
              color: Theme.of(context).colorScheme.onBackground),
          tooltip: S.of(context).settingsLabel,
          onPressed: () {
            Navigator.of(context).pushNamed(NavigationOptions.settingsRoute);
          },
        )
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
